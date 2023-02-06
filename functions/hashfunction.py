import hashlib
import os

"""Create a hash of a file. it is important to open file in 'rb' mode, reading in chunks makes it efficient for handling large files."""


def create_hash(file_path):
    if not os.path.exists(file_path) and os.path.isfile(file_path):
        return None
    with open(file_path, "rb") as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    print(file_hash.digest())
    print(file_hash.hexdigest())  # to get a printable str instead of bytes
    return file_hash.hexdigest()