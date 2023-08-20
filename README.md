# File2QR

Tools for transfering a file via QR codes.
There is a sender (program that creates QR codes) and a receiver (parses and reassembles QR codes).
They speak a common protocol, so you could for example use the React sender with the Python receiver.

Example usecases:

- (Auto) type the python client (`qrencode-server.min.py`) into a Kali VM that has not internet access and can only be accessed via restrictive means (remote access with no clipboard sharing, shared folders, etc).
    Then you can use the sender to exfiltrate results back to your computer.
- Generate QR codes for some important file (GPG key / password database), print them and store them in a safe place as an offline non-digital backup.
    Just make sure to encrypt the data beforehand if it is sensitive.

## Python

The simplest way to install it is with pip:
```bash
pip install qr2file
```

But of course you can also install it manually:

1. Clone this repository and open a shell in it.
2. If you want to have a `qr2file` script for this application, install it with pip:
    ```bash
    pip install ./python-client/
    ```

    Otherwise just install the dependencies:
    ```bash
    pip install -r ./python-client/requirements.in
    ```

### Receiver 

It should work on Linux (if you install a supported screenshot tool - currently only `scrot` / `grim`) and MacOS.

If installed with pip you can use `qr2file`:
```bash
qr2file -o ~/Downloads
```

You can also always manually call the script:
```bash
python3 ./python-client/src/main.py -o ~/Downloads
```

### Sender

A small single file tools, so that you could easily transfer to an target system.
It should work on Linux systems.
It relies on `qrencode` for actually creating the QR codes, so you may need to install that tool.

Usage:
```bash
file2qr /path/to/file /path/to/another-file
```

Or if you did not install it:
```bash
python3 ./python-client/src/file_to_qr/main.py /path/to/file /path/to/another-file
```

Generate QR codes as image files:
```bash
file2qr -o ~/Documents/qr-codes-for-file/ /path/to/file
```

Use the `--help` flag to see some performance tweaking options (QR code size and delay between codes).

`qrencode-server.min.py` is a minified version that can be faster transmitted to the target system via autotype / manually typing it.
See the usage by calling it without parameters.


## React sender

You can either self host it, or use the version deployed via Vercel at [react-file2qr.vercel.app](https://react-file2qr.vercel.app/?lang=en).
It should work cross platform with any modern browser (but probably not with Internet Explorer).

## Protocol

This section describes how data is encoded during the transfer.

### Transfer

The serialized data used to transmit a whole file is called a `transfer`.
It has the following structure:

Field | Length in bytes | Description
---|---|---
Version | 1 | Always `0x01`, used for future format changes
Name length | 4 | uint32 (big endian). Length of the following string.
Name | Value of `Name length` | The name of the file to be transmitted. **MUST NOT** contain path separators
Contents length | 4 | uint32 (big endian). Length of the following string.
Contents | Value of `Contents length` | The contents of the file to be transmitted

### Frame

The `transfer` is broken down into chunks called `frame`s that are small enough to fit into QR codes.
Each QR code will contain exactly one `frame` as content.
Each `frame` has the following structure:

Field | Length in bytes | Description
---|---|---
Version | 1 | Always `0x01`, used for future format changes
Transfer hash | 20 | SHA1 hash of the entire `transfer` object
Offset | 4 | uint32 (big endian). Offset of the data in the `transfer`
Data | All remaining bytes in frame | Slice of the `transfer`

### Design considerations

- QR codes have error correction built in, so we do not need any.
- `frames` can be sent in any order, duplicate frames do not matter.
    Thus it may be useful for the client to repeat the whole sequence in case the receiver had problems receiving some of the frames.
- Each `frame` is tagged with a tranfer hash (basically an UID), so that you can receive multiple `transfer`s at once.
- Receivers **MUST** check the transfer's file name for path separators and reject the transfer if found.
    Otherwise there may be path traversal vulnerabilities.
    For example a file name of `../../../../../home/USERNAME/.zshrc` could otherwise be used to replace the shell configuration file and gain code execution.
- Receivers **MUST** assume a malicious sender and should not blindly trust the values of length fields sent by the client.
    In languages like C it **MUST** be ensured, that no buffer overflow will happen, if the declared length is lower than the length of the actual data.
- Receivers should probably verify the transfer hash when the transfer is done, to make sure that the file was correctly received.

### Example

To see an example implementation of a sender, you can look at `qrencode-server.py`.
If you create a receiver/sender in a different language feel free to open a PR to add the code to this repo, or at least to link to your project :)

## Debugging QR code

[Qr2clipboard](https://gitlab.com/six-two/bin/-/blob/main/general/copy-qr-code) and then:
```
xclip -o -selection clipboard -rmlastnl | base64 -d | hexdump -C | less
```

