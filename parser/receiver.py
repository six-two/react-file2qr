#!/usr/bin/env python3
import argparse
import base64
import os
import subprocess
import sys
import time
from typing import Optional, Any, NamedTuple
from xml.dom import minidom
import bisect
import hashlib
# pip install Pillow
from PIL import Image
# pip install pyzbar
from pyzbar import pyzbar

QR_FILE = "/tmp/qr-receiver.png"
OUTPUT_FOLDER = "/tmp/qr-receiver/"

class V1Frame(NamedTuple):
    version: int
    hash: bytes
    offset: int
    data: bytes


class Chunk(NamedTuple):
    offset: int
    data: bytes

    def __lt__(self, other):
        if type(other) == int:
            return self.offset < other
        else:
            return self.offset < other.offset

# not very robust against forged qr codes, but who cares :)
class DataReassembly:
    def __init__(self, data_hash: bytes):
        self.chunks = []
        self.hash = data_hash

    def add_chunk(self, new_offset: int, new_data: bytes) -> None:
        new_chunk = Chunk(new_offset, new_data)
        i = bisect.bisect_left(self.chunks, new_offset)
        if i != len(self.chunks) and self.chunks[i].offset == new_offset:
            old = self.chunks[i]
            if len(new_chunk.data) >= len(old.data):
                self.chunks[i] = new_chunk
        else:
            bisect.insort(self.chunks, new_chunk)

    def get_data_if_complete(self) -> Optional[bytes]:
        data = b""
        for chunk in self.chunks:
            # there should be no overlaps, so it should be irelevant which data I use
            start = chunk.offset
            end = start + len(chunk.data)
            if start <= len(data):
                if end > len(data):
                    data = data[:start] + chunk.data
            else:
                break

        digest = hashlib.sha1()
        digest.update(data)
        hashed_data = digest.digest()
        # print("=== Hashes ===")
        # print(hashed_data)
        # print(self.hash)

        return data if hashed_data == self.hash else None


def bytes_to_int32(data: bytes) -> int:
    value = 0
    # print("data:", data.hex())
    # print(len(data))
    value += data[0] << 24
    value += data[1] << 16
    value += data[2] << 8
    value += data[3]
    return value


def parse_v1_frame(payload: bytes) -> Optional[V1Frame]:
    i = 0
    # print("payload", payload[:40].hex()+"...")
    version, i = payload[i], i + 1
    if version != 1:
        return None
    hash, i = payload[i:i+20], i + 20
    offset_bytes, i = payload[i:i+4], i + 4
    data = payload[i:]
    offset = bytes_to_int32(offset_bytes)
    return V1Frame(version, hash, offset, data)


def read_binary_qr_code(input_file: str) -> bytes:
    return subprocess.check_output(["zbarimg", "--quiet", "--raw", "-Sbinary", input_file])


def parse_qr(input_file: str) -> list[bytes]:
    if not os.path.exists(input_file):
        notify("No screenshot was taken", "Error")
        sys.exit(1)

    # try:
    #     output = subprocess.check_output(["zbarimg", "--quiet", "--xml", input_file])
    # except subprocess.CalledProcessError as e:
    #     print(e)
    #     output = e.output
    # print(output)
    # output = output.decode("utf-8", errors="ignore")
    # print(output)
    # parser = minidom.parseString(output)
    # tag_list = parser.getElementsByTagName('data')
    # data_list = [tag.firstChild.wholeText.strip() for tag in tag_list]
    # return data_list

    img = Image.open(input_file)
    decoded = pyzbar.decode(img, symbols=[pyzbar.ZBarSymbol.QRCODE])
    results = []
    for code in decoded:
        # print(code)
        x, y, w, h = code.rect
        # print(x, y, w, h)
        cropped = img.crop((x, y, x+w, y+h))
        # cropped.show()
        # code.data is buggy, since it is null terminated. So i need to extract the QR codes and decode them individualy
        cropped.save(QR_FILE)
        try:
            results.append(read_binary_qr_code(QR_FILE))
        except Exception as ex:
            print(ex)

    return results


def notify(message: str, title: str) -> None:
    print("Notification:", message)
    subprocess.call(["notify-send", "--expire-time", "3000", title, message])


def take_screenshot(output_file: str) -> None:
    if os.path.exists(output_file):
        os.remove(output_file)
    print("Taking screenshot")
    subprocess.check_call(["scrot", output_file])


def transfer_finished(data: bytes) -> None:
    print("Transfer finished")
    # print(data.hex())

    i = 0
    # read file name length
    name_length = bytes_to_int32(data[i:i+4])
    i += 4
    # read file name
    name = data[i:i+name_length]
    i += name_length
    # read file data length
    contents_length = bytes_to_int32(data[i:i+4])
    i += 4
    # read file data
    contents = data[i:i+contents_length]
    i += contents_length

    if i != len(data):
        print(f"Length mismatch: expected {i}, got {len(data)}")

    name = name.decode("utf-8")
    print("Name:", name)
    print("Contents:", contents.hex())

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    with open(os.path.join(OUTPUT_FOLDER, name), "wb") as f:
        f.write(contents)


def parse_args() -> Any:
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--sleep", type=int, help="the number of millis to sleep between screenshots", default=900)
    return ap.parse_args()

def main():
    args = parse_args()
    chunks = {} # hash -> list[data]  
    sleep = args.sleep / 1000

    try:
        while True:
            start = time.monotonic()
            take_screenshot(QR_FILE)
            data_list = parse_qr(QR_FILE)
            # print(data_list)
            for data in data_list:
                parsed = parse_v1_frame(data)
                if parsed:
                    # print(parsed._replace(data="[...]"))
                    hash = parsed.hash.hex()
                    chunk = chunks.get(parsed.hash)
                    if not chunk:
                        chunk = DataReassembly(parsed.hash)
                        chunks[parsed.hash] = chunk
                    chunk.add_chunk(parsed.offset, parsed.data)
                    print(parsed.hash.hex(), parsed.offset)

                    try_assemble = chunk.get_data_if_complete()
                    if try_assemble:
                        transfer_finished(try_assemble)
                        sys.exit(0)
                else:
                    print("Failed to parse contents")
            diff = time.monotonic() - start
            remaining = sleep - diff
            remaining > 0 and time.sleep(remaining)
    except KeyboardInterrupt:
        print("<Ctrl-C>")


if __name__ == "__main__":
    main()
