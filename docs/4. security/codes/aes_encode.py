from Crypto.Cipher import AES
import io
import os
import hashlib
import binascii
IMAGE_IV = b'0000000000000000' # IV는 이 값을 사용
aes_key = binascii.hexlify(os.urandom(16)) # 랜덤하게 키값 생성

def aes_encode(mem_file, aes_key):
    iv = IMAGE_IV
    mem_file.seek(0)
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    raw = mem_file.read()
    last_length = len(raw) % 16
    if last_length != 0:
        raw += (b' ' * (16 - last_length) )
    ret_file = io.BytesIO(cipher.encrypt(raw))
    ret_file.seek(0)
    return ret_file

def aes_decode(mem_file, aes_key):
    key = aes_key
    iv = IMAGE_IV
    cipher = AES.new(key, AES.MODE_CBC, IV=iv)
    raw = cipher.decrypt(mem_file.read())
    last_length = len(raw) % 16
    if last_length == 0:
        ret_file = io.BytesIO(raw)
        ret_file.seek(0)
        return ret_file
    # padding
    raw = raw.decode('utf-8').strip().encode('utf-8')
    ret_file = io.BytesIO(raw)
    ret_file.seek(0)
    return ret_file

# 이미지 파일 읽어와서 AES-128로 암호화 하기 
with open('test_image.jpg', 'rb') as fp:
    t = aes_encode(fp, aes_key)

# 암호화 한 이미지 파일로 쓰기, 나중에 인식 요청시 encrypted_image.jpg 파일 정보를 전달
with open('encrypted_image.jpg', 'wb') as fp:
    fp.write( t.read())

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from base64 import b64decode,b64encode

pubkey = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuxqUjkLk04AJjSswWGzXZp76fVUYI0wbAPsWD2Es5S2uvcpMnhFOS//HdOZaDHgPrPsqgE9zUuiaOE1aw1e1OX64QWLlnQRlBJKEDAG2aFWxrdmq19LDjVx/1XAJxhilPCnW0g0PdOT9CZz9bxmnHSjYeU3EMWsB9gVWYCn6hO31Fu4BaB6s9i8vSWDiqF3BDuAjY39Ir4V6b6YY0txqGEWhkLD+Aj2XY1wpSxL7giANoRWrTcN/3taC3YVNoyNAZ/sS9B0q2+wAm3FBvXV63tYZvmQSk4UEhwPoRe9UfWb1rqKCQPPns5elY73Lb+fU5Fy3B7wPAgw+WKjNYJePvQIDAQAB' # /api/v1/key 호출로 얻어온 값
keyDER = b64decode(pubkey)
keyPub = RSA.importKey(keyDER)
cipher = Cipher_PKCS1_v1_5.new(keyPub)
cipher_text = cipher.encrypt(aes_key)
emsg = b64encode(cipher_text) # emsg 값을 인식 요청 헤더에 같이 전달
