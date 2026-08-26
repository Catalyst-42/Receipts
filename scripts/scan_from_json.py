import asyncio
import json
import warnings
from pathlib import Path

import requests

warnings.filterwarnings("ignore")


def process_single_item(
    qr_code: str, api_base_url: str, index: int, total: int
) -> bool:
    print(f"\r{index}/{total}", end=" ", flush=True)

    if not qr_code:
        return False

    verify_ssl = False

    response = requests.post(
        f"{api_base_url}/registry?{qr_code}",
        verify=verify_ssl,
    )
    response.raise_for_status()
    return response.status_code == 200 and response.json().get("success")


async def process_json_file(json_path: str, api_base_url: str) -> None:
    json_file = Path(json_path)
    if not json_file.exists():
        print("\rJSON file not found")
        return

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        print("\rJSON root must be a list")
        return

    qr_codes = []
    for item in data:
        code = item.get("data", {}).get("code")
        if code:
            qr_codes.append(code)

    if not qr_codes:
        print("\rNo QR codes found in JSON")
        return

    successful = 0
    total = len(qr_codes)
    for i, qr_code in enumerate(qr_codes, 1):
        if process_single_item(qr_code, api_base_url, i, total):
            successful += 1

    print(f"\rDone with {successful} successful of {total}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Process QR codes from JSON file and import receipts via current app API. "
        "JSON must be a list of objects with 'data.code' field containing the QR code string."
    )
    parser.add_argument("json_file", help="Path to JSON file with QR codes")
    parser.add_argument(
        "--api-url",
        default="https://localhost:8800",
        help="Receipts API base URL (default: https://localhost:8800)",
    )
    args = parser.parse_args()
    asyncio.run(process_json_file(args.json_file, args.api_url))
