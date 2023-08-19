#!/usr/bin/env python3
from hashlib import sha1
from subprocess import run
import time
from sys import argv as a
import os

def i2b(n):
    return n.to_bytes(4, 'big')

def tfr(d, n, cs, ds):
    v = b"\x01"
    nb = n.encode()
    sf = v + i2b(len(nb)) + nb + i2b(len(d)) + d
    th = sha1(sf).digest()
    for o in range(0, len(sf), cs):
        offset_bytes = i2b(o)
        data_slice = sf[o:o+cs]
        fd = v + th + i2b(o) + sf[o:o+cs] 
        
        run("clear")
        print(f"[*] {o}/{len(sf)}")
        run(["qrencode", "-t", "ANSI256UTF8", "-m", "2", "-8"], input=fd)
        time.sleep(ds)

al = len(a)
if al < 2:
    print("Usage: <input_file> [chunk_size] [delay_seconds]")
else:
    with open(a[1], "rb") as f:
        d = f.read()
    cs = int(a[2]) if al > 2 else 1000
    ds = float(a[3]) if al > 3 else 1
    n = os.path.basename(a[1])
    tfr(d, n, cs, ds)
