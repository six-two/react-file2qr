import { createHash } from 'sha1-uint8array';

export const serializeFile = (name: string, content_bytes: Uint8Array) => {
    const name_bytes = new TextEncoder().encode(name);
    const name_length_bytes = int32ToBytes(name_bytes.length);
    const content_length_bytes = int32ToBytes(content_bytes.length);
    const result = new Uint8ClampedArray([...name_length_bytes, ...name_bytes, ...content_length_bytes, ...content_bytes]);
    return new Uint8Array(result);
}

export class HashedData {
    data: Uint8Array;
    hash: Uint8Array;

    constructor(data: Uint8Array) {
        this.data = data;
        this.hash = createHash().update(data).digest();
    }
}

const getByte = (multiByteNumber: number, byteIndex: number) => {
    return (multiByteNumber >> (8 * byteIndex)) & 255;
}

const int32ToBytes = (int32: number) => {
    return [getByte(int32, 3), getByte(int32, 2), getByte(int32, 1), getByte(int32, 0)];
}

export const addQrHeadersToDataSlice = (data: HashedData, start_index: number, end_index: number) => {
    const version = [1];
    const hash = data.hash.values();
    const offset_bytes = int32ToBytes(start_index);
    const data_bytes = data.data.slice(start_index, end_index);
    const data_with_headers = [...version, ...hash, ...offset_bytes, ...data_bytes];
    return new Uint8Array(new Uint8ClampedArray(data_with_headers));
}

