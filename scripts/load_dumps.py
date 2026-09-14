import asyncio
import json
import re
import warnings
from pathlib import Path

import cv2
import requests
from pyzbar import pyzbar

warnings.filterwarnings("ignore")

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff"}
QR_PATTERN = re.compile(r't=.+&s=.+&fn=.+&i=.+&fp=.+&n=.+')


def qr_code(image_path: str) -> str:
    image = cv2.imread(image_path)
    if image is None:
        return ""
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    barcodes = pyzbar.decode(image)
    return barcodes[0].data.decode("utf-8") if barcodes else ""


def send_request(qr_code_str: str, api_base_url: str, token: str) -> bool:
    if not qr_code_str:
        return False
    response = requests.post(f"{api_base_url}/registry/by-fiscal-fields?{qr_code_str}", verify=False, headers={
        "Authorization": f"Bearer {token}"
    })
    response.raise_for_status()
    return response.status_code == 200


async def main(path: str, api_base_url: str, token: str) -> None:
    root = Path(path)
    qr_codes = []

    if root.is_dir():
        files = list(root.rglob("*"))
    elif root.is_file():
        files = [root]
    else:
        print("Path does not exist")
        return

    for file in files:
        if not file.is_file():
            continue
        ext = file.suffix.lower()
        if ext in IMAGE_EXTS:
            code = qr_code(str(file))
            if code:
                qr_codes.append(code)
        elif ext == ".json":
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                qr_codes.extend(data.get("qr_codes", []))
        elif ext == ".txt":
            with open(file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line and QR_PATTERN.match(line):
                    qr_codes.append(line)

    if not qr_codes:
        print("No QR codes found")
        return

    successful = 0
    total = len(qr_codes)
    for i, code in enumerate(qr_codes, 1):
        print(f"\r{i}/{total}", end=" ", flush=True)
        if send_request(code, api_base_url, token):
            successful += 1

    print(f"\rDone with {successful} successful of {total}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Process QR codes from images, JSON files, and TXT files (recursively)"
    )
    parser.add_argument("path", help="Directory or file (image, JSON, or TXT)")
    parser.add_argument(
        "token",
        help="Authorization token for API access",
    )
    parser.add_argument(
        "--api-url",
        default="https://localhost:8800",
        help="Receipts API base URL (default: https://localhost:8800)",
    )
    args = parser.parse_args()
    asyncio.run(main(args.path, args.api_url, args.token))
