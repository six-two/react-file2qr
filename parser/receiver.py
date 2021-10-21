#!/usr/bin/env python3
import argparse
import subprocess
import time
from typing import Any
# local modules
from assembler import ReassemblyManager
from qr import take_screenshot, parse_qr

QR_FILE = "/tmp/qr-receiver.png"
OUTPUT_FOLDER = "/tmp/qr-receiver/"


def notify(message: str, title: str) -> None:
    print("Notification:", message)
    subprocess.call(["notify-send", "--expire-time", "3000", title, message])


def parse_args() -> Any:
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--sleep", type=int, help="the number of millis to sleep between screenshots", default=900)
    return ap.parse_args()

def main():
    args = parse_args()
    assembler = ReassemblyManager(OUTPUT_FOLDER)
    sleep = args.sleep / 1000

    try:
        while True:
            start = time.monotonic()
            take_screenshot(QR_FILE)
            data_list = parse_qr(QR_FILE)
            for data in data_list:
                assembler.add_data_chunk(data)
            diff = time.monotonic() - start
            remaining = sleep - diff
            remaining > 0 and time.sleep(remaining)
    except KeyboardInterrupt:
        print("<Ctrl-C>")


if __name__ == "__main__":
    main()
