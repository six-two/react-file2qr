import os
import subprocess
import sys
# pip install Pillow
from PIL import Image
# pip install pyzbar
from pyzbar import pyzbar

TMP_FILE = "/tmp/qr-receiver-tmp.png"


def parse_qr(input_file: str) -> list[bytes]:
    if not os.path.exists(input_file):
        raise Exception(f"File '{input_file}' does not exist")

    img = Image.open(input_file)
    qr_code_list = pyzbar.decode(img, symbols=[pyzbar.ZBarSymbol.QRCODE])
    qr_code_list = list(qr_code_list)

    if not qr_code_list:
        return []
    elif len(qr_code_list) == 1:
        return [read_binary_qr_code(input_file)]
    else:
        results = []
        for code in qr_code_list:
            code_contents = extract_and_read_qr_code(code)
            if code_contents:
                results.append(code_contents)
        return results


def extract_and_read_qr_code(code) -> bytes:
    x, y, w, h = code.rect
    cropped = img.crop((x, y, x+w, y+h))
    # code.data is buggy, since it is null terminated. So i need to extract the QR codes and decode them individualy
    cropped.save(TMP_FILE)
    try:
        return read_binary_qr_code(TMP_FILE)
    except Exception as ex:
        print(ex)
        return None


def read_binary_qr_code(input_file: str) -> bytes:
    return subprocess.check_output(["zbarimg", "--quiet", "--raw", "-Sbinary", input_file])


def take_screenshot(output_file: str) -> None:
    if os.path.exists(output_file):
        os.remove(output_file)
    # print("Taking screenshot")
    subprocess.check_call(["scrot", output_file])
