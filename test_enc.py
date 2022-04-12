
from cryptography.fernet import Fernet
import struct


BLOCK = 1 << 16


class CRT:

    _key_name = ''
    _pth = ''

    def __init__(self):
        try:
            key = self.key_load()
        except Exception:
            key = self.key_create()
            self.key_write(key)

        self._key = key

    def key_create(self):
        key = Fernet.generate_key()
        return key

    def key_write(self, key):
        with open(self._key_name, 'wb') as mykey:
            mykey.write(key)

    def key_load(self):
        with open(self._key_name, 'rb') as mykey:
            key = mykey.read()
        return key

    def file_encrypt(self, filename, ):
        f = Fernet(self._key)

        with open(self._pth % filename, 'rb') as in_file, open(self._pth % (filename + 'e'), 'wb') as out_file:
            while True:
                chunk = in_file.read(BLOCK)
                if len(chunk) == 0:
                    break
                enc = f.encrypt(chunk)
                out_file.write(struct.pack('<I', len(enc)))
                out_file.write(enc)
                if len(chunk) < BLOCK:
                    break

    def file_decrypt(self, filename):
        f = Fernet(self._key)

        with open(self._pth % filename, 'rb') as in_file, open(self._pth % (filename + 'e'), 'wb') as out_file:
            while True:
                size_data = in_file.read(4)
                if len(size_data) == 0:
                    break
                chunk = in_file.read(struct.unpack('<I', size_data)[0])
                dec = f.decrypt(chunk)
                out_file.write(dec)
