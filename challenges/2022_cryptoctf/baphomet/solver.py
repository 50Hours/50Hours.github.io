from base64 import b64encode, b64decode
from Crypto.Util.number import long_to_bytes
def xor(msg, key):
    enc = b''
    for i in range(len(msg)):
        enc += (msg[i] ^ key[i % len(key)]).to_bytes(1, 'big')
    return enc

def convert(msg):
    ret = b''
    for c in msg.decode('utf-8'):
        if c.islower():
            ret += c.upper().encode()
        else:
            ret += c.lower().encode()
    return ret
        
with open('flag.enc', 'rb') as file:
    enc = file.read()

assert len(enc) == 48
key_len = len(enc) // 8
print(key_len)

prefix = b64encode(b'CCTF{')
prefix_real = convert(prefix)
print(prefix_real)

key = b''

for u, v in zip(prefix_real, enc):
    key += long_to_bytes(u ^ v)

key = key[:6]
print(b64decode(convert(xor(enc, key))))
# CCTF{UpP3r_0R_lOwER_17Z_tH3_Pr0bL3M}