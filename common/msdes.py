# Microsoft Standard DES Encrypt and Decrypt Algorithm.
import base64
import pyDes
import six

class DES:
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv

    def encrypt(self, data):
        des = pyDes.des(self.key, mode=pyDes.CBC, IV=self.iv, pad=None, padmode=pyDes.PAD_PKCS5)
        if isinstance(data, six.string_types):
            data = bytes(data, 'utf-8')
        enc = des.encrypt(data)
        return base64.encodebytes(enc).decode('utf-8')

    def decrypt(self, data):
        des = pyDes.des(self.key, mode=pyDes.CBC, IV=self.iv, pad=None, padmode=pyDes.PAD_PKCS5)
        if isinstance(data, six.string_types):
            data = bytes(data, 'utf-8')
        data = base64.decodebytes(data)
        return des.decrypt(data).decode('utf-8')


if __name__ == '__main__':
    nd = DES('12345678', '87654321')
    k = nd.encrypt('AAA@111')
    print(k)
    print(nd.decrypt(k.strip()))
