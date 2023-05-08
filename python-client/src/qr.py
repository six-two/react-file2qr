import os
import shutil
import subprocess
import tempfile
from typing import Optional
# pip install Pillow
from PIL import Image
# pip install pyzbar
from pyzbar import pyzbar


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
            code_contents = extract_and_read_qr_code(code, img)
            if code_contents:
                results.append(code_contents)
        return results


def extract_and_read_qr_code(code, img: Image) -> Optional[bytes]:
    _, tmp_file = tempfile.mkstemp()
    x, y, w, h = code.rect
    cropped = img.crop((x, y, x+w, y+h))
    # code.data is buggy, since it is null terminated. So i need to extract the QR codes and decode them individualy
    cropped.save(tmp_file)
    try:
        return read_binary_qr_code(tmp_file)
    except Exception as ex:
        print(ex)
        return None
    finally:
        os.remove(tmp_file)


def read_binary_qr_code(input_file: str) -> bytes:
    return subprocess.check_output(["zbarimg", "--quiet", "--raw", "-Sbinary", input_file])


def take_screenshot(output_file: str) -> None:
    if os.path.exists(output_file):
        os.remove(output_file)

    command = generate_screenshot_command(output_file, False)
    subprocess.call(command)

    if not os.path.exists(output_file):
        raise Exception(f"Command {command} did not produce output file {output_file}")


def generate_screenshot_command(output_file: str, user_selects_area: bool):
    # @SOURE/@SYNC https://gitlab.com/six-two/bin/-/blob/main/general/copy-qr-code
    if shutil.which("scrot"):
        # The scrot screenshot tool is installed
        if user_selects_area:
            return ["scrot", "-s", output_file]
        else:
            return ["scrot", output_file]
    elif shutil.which("screencapture"):
        # This tool is installed on MacOS by default. You may need to allow 'Terminal' to record your screen (it should pop up a dialog)
        # Only tested in a single monitor setup, you may need to replace "-m" with something like "-D 2" to select the correct screen
        if user_selects_area:
            return ["screencapture", "-i", "-J", "selection", output_file]
        else:
            return ["screencapture", "-m", output_file]
    else:
        print("[!] No supported screenshot tool installed.")
        print("Please install 'scrot' or add your screenshot tool to the 'generate_screenshot_command' function in 'python-client/src/qr.py'")
        raise Exception("Missing external dependency: screenshot tool")
