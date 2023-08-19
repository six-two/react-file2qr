import bisect
import hashlib
import os
from typing import NamedTuple, Optional
# local modules
from .protocol import V1Transfer, parse_v1_transfer, parse_v1_frame


class Chunk(NamedTuple):
    offset: int
    data: bytes

    def __lt__(self, other):
        return self.offset < other.offset

# not very robust against forged qr codes, but who cares :) I mean it is hashed, so I should be fine
class TransferReassembly:
    def __init__(self, data_hash: bytes):
        self.chunks: list[Chunk] = []
        self.hash = data_hash
        self.complete_data: Optional[bytes] = None

    def add_chunk(self, chunk: Chunk) -> bool:
        """Returns True, if the internal state was changed"""
        i = bisect.bisect_left(self.chunks, chunk)
        if i != len(self.chunks) and self.chunks[i].offset == chunk.offset:
            # a chunk with the same offset already exists
            old = self.chunks[i]
            if old.data == chunk.data:
                return False
            elif len(chunk.data) >= len(old.data):
                self.chunks[i] = chunk
        else:
            # no chunk with the same offset exists
            bisect.insort(self.chunks, chunk)

        self.complete_data = self.get_data_if_complete()
        return True

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

        hashed_data = hashlib.sha1(data).digest()
        return data if hashed_data == self.hash else None


class ReassemblyManager:
    def __init__(self, output_folder: str) -> None:
        self.transfers: dict[bytes,TransferReassembly] = {}
        self.output_folder = output_folder

    def add_data_chunk(self, data: bytes) -> None:
        frame = parse_v1_frame(data)
        transfer = self.transfers.get(frame.transfer_hash)
        if not transfer:
            transfer = TransferReassembly(frame.transfer_hash)
            self.transfers[frame.transfer_hash] = transfer

        chunk = Chunk(frame.transfer_offset, frame.data)
        if transfer.add_chunk(chunk):
            self.on_new_chunk(frame.transfer_hash, chunk)
            if transfer.complete_data:
                result = parse_v1_transfer(transfer.complete_data, frame.transfer_hash)
                self.on_transfer_completed(result)

    def on_new_chunk(self, transfer_hash: bytes, chunk: Chunk) -> None:
        end = chunk.offset + len(chunk.data) - 1
        print(f"{transfer_hash.hex()} | {chunk.offset}..{end}")

    def on_transfer_completed(self, transfer: V1Transfer):
        print(f"{transfer.transfer_hash.hex()} | Transfer finished: {transfer.name}")
        os.makedirs(self.output_folder, exist_ok=True)

        # The last check is just in case there is a system that has really strange path separators
        if "/" in transfer.name or "\\" in transfer.name or os.path.sep in transfer.name:
            # Path traversal detection
            print(f"[!] Security warning: Name '{transfer.name}' contains a path separator. This may be an attack! The transfer has been discarded")
        else:
            out_file = os.path.join(self.output_folder, transfer.name)
            with open(out_file, "wb") as f:
                f.write(transfer.contents)
            
            print(f"Received file: {out_file} ({round(len(transfer.contents) / 1024.0, 2)} KiB)")
