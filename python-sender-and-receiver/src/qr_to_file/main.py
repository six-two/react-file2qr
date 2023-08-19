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
    return ap.parse_args()

def main():
    args = parse_args()
    if not os.path.isdir(args.output_dir):
        print(f"Output directory '{args.output_dir}' is not a directory or does not exist")
        exit(1)
    assembler = ReassemblyManager(args.output_dir)
    sleep = args.sleep / 1000
    print(f"[*] Taking screenshots every {sleep} seconds. Open the web app at https://react-file2qr.vercel.app/ and start the QR slide show (or use qr2file). Exit receiving with Ctrl-C")
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
            remaining = sleep - diff
            remaining > 0 and time.sleep(remaining)
    except MissingProgramException as ex:
        print(f"\n\n[!] MissingProgramException: {ex}")
    except KeyboardInterrupt:
        print("<Ctrl-C>")
    finally:
        if os.path.exists(qr_file):
            os.remove(qr_file)


if __name__ == "__main__":
    main()
