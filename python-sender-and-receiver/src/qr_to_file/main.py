#!/usr/bin/env python3
import argparse
import os
import subprocess
import tempfile
import time
from typing import Any
# local modules
from .assembler import ReassemblyManager
from .qr import take_screenshot, parse_qr, MissingProgramException

DEFAULT_OUTPUT_FOLDER = "/tmp/qr-receiver/"


def notify(message: str, title: str) -> None:
    print("Notification:", message)
    subprocess.call(["notify-send", "--expire-time", "3000", title, message])


def parse_args() -> Any:
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--sleep", type=int, help="the number of millis to sleep between screenshots", default=900)
    ap.add_argument("-o", "--output-dir", default=DEFAULT_OUTPUT_FOLDER, help=f"the folder to write the results to (default: {DEFAULT_OUTPUT_FOLDER})")
    ap.add_argument("-i", "--images", nargs="+", help="instead of taking regular screenshots, read all the given image files")
    ap.add_argument("-w", "--webcam", metavar="WEBCAM_ID", type=int, help="instead of taking screenshots, take pictures with a webcam. Usually 0 or 1 should be the ID of your first webcam")
    return ap.parse_args()

def main_loop_with_screenshots(assembler: ReassemblyManager, sleep_seconds: float):
    print(f"[*] Taking screenshots every {sleep_seconds} seconds. Open the web app at https://react-file2qr.vercel.app/ and start the QR slide show (or use qr2file). Exit receiving with Ctrl-C")
    print("[*] Hint: You will see output, when a new QR code containing a file segment is parsed")
    print("\n----------------- Hash ----------------- | --- Bytes received ---")

    _, qr_file = tempfile.mkstemp()
    try:
        while True:
            start = time.monotonic()
            take_screenshot(qr_file)
            data_list = parse_qr(qr_file)
            for data in data_list:
                assembler.add_data_chunk(data)
            diff = time.monotonic() - start
            remaining = sleep_seconds - diff
            if remaining > 0:
                time.sleep(remaining)
    except MissingProgramException as ex:
        print(f"\n\n[!] MissingProgramException: {ex}")
    except KeyboardInterrupt:
        print("<Ctrl-C>")
    finally:
        if os.path.exists(qr_file):
            os.remove(qr_file)


def main_loop_with_images(assembler: ReassemblyManager, image_file_list: list[str]):
    print(f"[*] Parsing {len(image_file_list)} image files")
    print("[*] Hint: You will see output, when a new QR code containing a file segment is parsed")
    print("\n----------------- Hash ----------------- | --- Bytes received ---")

    for image_file in image_file_list:
        if not os.path.exists(image_file):
            print(f"[-] File '{image_file}' does not exist")
        else:
            data_list = parse_qr(image_file)
            for data in data_list:
                assembler.add_data_chunk(data)

    print("[*] Done - all image files were processed")


def main():
    args = parse_args()
    if not os.path.isdir(args.output_dir):
        print(f"Output directory '{args.output_dir}' is not a directory or does not exist")
        exit(1)
    assembler = ReassemblyManager(args.output_dir)
    if args.images:
        image_file_list = args.images if type(args.images) == list else [args.images]
        main_loop_with_images(assembler, image_file_list)
    elif args.webcam is not None:
        # Conditional import. Only actually import opencv if we want/need to use it
        from .webcam import main_loop_with_webcam
        sleep_seconds = args.sleep / 1000
        main_loop_with_webcam(assembler, sleep_seconds, args.webcam)
    else:
        sleep_seconds = args.sleep / 1000
        main_loop_with_screenshots(assembler, sleep_seconds)


if __name__ == "__main__":
    main()
