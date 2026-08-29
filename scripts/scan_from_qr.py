import asyncio
import warnings
from pathlib import Path

import cv2
import requests
from pyzbar import pyzbar

warnings.filterwarnings("ignore")


def qr(image_path: str) -> str:
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    barcodes = pyzbar.decode(image)
    return barcodes[0].data.decode("utf-8") if barcodes else ""


async def process_single_image(
    image_path: str, api_base_url: str, index: int, total: int
) -> bool:
    print(f"\r{index}/{total}", end=" ", flush=True)

    qr_code = qr(image_path)
    if not qr_code:
        return False

    verify_ssl = False

    response = requests.delete(f"{api_base_url}/registry?{qr_code}", verify=verify_ssl)
    return response.status_code == 200


async def process_qr_images_directory(directory: str, api_base_url: str) -> None:
    directory_path = Path(directory)
    image_extensions = {".png", ".jpg", ".jpeg", ".bmp", ".tiff"}

    image_files = []
    for ext in image_extensions:
        image_files.extend(directory_path.glob(f"*{ext}"))
        image_files.extend(directory_path.glob(f"*{ext.upper()}"))

    if not image_files:
        print("\rNo image files found")
        return

    successful = 0
    for i, image_file in enumerate(sorted(image_files), 1):
        if await process_single_image(
            str(image_file), api_base_url, i, len(image_files)
        ):
            successful += 1

    print(f"\rDone with {successful} succesful of {len(image_files)}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Process QR code images and import receipts via current app API. Contains directory path to be processed and optionally a url of Receipts API",
    )
    parser.add_argument("directory", help="Directory containing QR code images")
    parser.add_argument(
        "--api-url",
        default="https://localhost:8800",
        help="Receipts API base URL (default: https://localhost:8800)",
    )
    args = parser.parse_args()
    asyncio.run(process_qr_images_directory(args.directory, args.api_url))
