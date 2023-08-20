# Optional: Capture images via webcam (for air-gapped systems that you are pysically close to)
# Point your (external) webcam to the target's screen and show the QR codes on it
import os
import tempfile
import time
# local modules
from .assembler import ReassemblyManager
from .qr import parse_qr, MissingProgramException
# pip install opencv-python
import cv2
# # pip install Pillow
# from PIL import Image


# Based roughly on https://stackoverflow.com/questions/43776606/direct-way-to-get-camera-screenshot
def main_loop_with_webcam(assembler: ReassemblyManager, sleep_seconds: float, webcam_id: int):
    print(f"[*] Taking webcam images every {sleep_seconds} seconds. Open the web app at https://react-file2qr.vercel.app/ and start the QR slide show (or use qr2file). Exit receiving with Ctrl-C")
    print("[*] Hint: You will see output, when a new QR code containing a file segment is parsed")
    print("\n----------------- Hash ----------------- | --- Bytes received ---")

    cam = cv2.VideoCapture(webcam_id)
    _, qr_file = tempfile.mkstemp(suffix=".png")
    print(f"[*] The current webcam image is at {qr_file}. You can view this file with an image viewer to see what the camera is seeing and see if the camera id, positioning, etc are correct")
    try:
        while True:
            start = time.monotonic()
            # take and convert image
            _, img = cam.read()
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # im_pil = Image.fromarray(img)
            # We need to have it as a file anyways, so no directly converting it yould only save us one PNG read but complicate the code
            cv2.imwrite(qr_file, img)

            # parse image
            data_list = parse_qr(qr_file)
            for data in data_list:
                assembler.add_data_chunk(data)
            
            # delay next iteration
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