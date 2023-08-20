#!/usr/bin/env python3
import argparse
import hashlib
import shutil
import subprocess
import time
from typing import Optional
import os


def int32_to_bytes(number: int) -> bytes:
    return number.to_bytes(4, 'big')

def transfer(data: bytes, name: str, chunk_size: int, delay_seconds: float, output_dir: Optional[str]) -> None:
    version = b"\x01"
    name_bytes = name.encode()
    name_bytes_len = int32_to_bytes(len(name_bytes))
    data_len = int32_to_bytes(len(data))
    serialized_file = version + name_bytes_len + name_bytes + data_len + data

    transfer_hash = hashlib.sha1(serialized_file).digest()
    print(f"[*] Transfering {transfer_hash.hex()} ({name}) - {len(data)} bytes")

    # @TODO delete old files (with same transfer id) when storing new images?

    for offset in range(0, len(serialized_file), chunk_size):
        offset_bytes = int32_to_bytes(offset)
        data_slice = serialized_file[offset:offset+chunk_size]
        frame_data = version + transfer_hash + offset_bytes + data_slice 

        if output_dir:
            # Store all QR codes in image files in the output directory
            if not os.path.isdir(output_dir):
                print(f"[!] '{output_dir}' is not a directory! Exiting...")
                exit(1)
            else:
                file_index = offset // chunk_size
                output_file_name = os.path.join(output_dir, f"{transfer_hash.hex()}_{file_index:03}.png")
                subprocess.run(["qrencode", "-m", "2", "-8", "-o", output_file_name], input=frame_data)
                # Show the progress. Each dot means a single file was generated
                print(".", end="", flush=True)
        else:
            # delete old qr code
            subprocess.call("clear")
            print(f"Sending {name} ({transfer_hash.hex()}): {offset+len(data_slice)}/{len(serialized_file)}")
            # show new qr code
            # -t ANSI256UTF8: smallest pixel representation
            # -m 2: smaller margin -> takes up less space
            # -8: needed for binary data to work
            subprocess.run(["qrencode", "-t", "ANSI256UTF8", "-m", "2", "-8"], input=frame_data)
            # wait before showing the next code
            time.sleep(delay_seconds)

    # Add a new-line after the dots being shown as the progress indicator
    if output_dir:
        print()


def main():
    if not shutil.which("qrencode"):
        print("[!] 'qrencode' program not found. It is needed to generate QR codes")
        exit(1)

    ap = argparse.ArgumentParser(description="Store the contents of a file in QR codes. This can be used to transfer a file between locked down citrix/RDP sessions or air-gapped systems. Use 'qr2file' to convert them back to the original file on the target system.")
    ap.add_argument("input_files", nargs="+", help="the file to transfer")
    ap.add_argument("-c", "--chunk-size", type=int, default=1000, help="how many file data to transmit per QR code")
    output_option_group = ap.add_mutually_exclusive_group()
    output_option_group.add_argument("-d", "--delay", type=float, default=1, help="how many seconds to wait between QR codes")
    output_option_group.add_argument("-o", "--output-dir", help="instead of showing QR codes, store them as image files in the given folder")
    args = ap.parse_args()

    # Check all files first so that it does not crash in the middle of transfering multiple files
    for input_file in args.input_files:
        if not os.path.exists(input_file):
            print(f"[!] '{input_file}' does not exist")
        if not os.path.isfile(input_file):
            print(f"[!] '{input_file}' is not a file")

    # Transfer the files
    try:
        for input_file in args.input_files:
            with open(input_file, "rb") as f:
                data = f.read()
            name = os.path.basename(input_file)
            transfer(data, name, args.chunk_size, args.delay, args.output_dir)
    except KeyboardInterrupt:
        print("\n[Ctrl-C] Stopped transfers")

if __name__ == "__main__":
    main()
