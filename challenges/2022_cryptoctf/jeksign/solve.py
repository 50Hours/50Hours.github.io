from random import getrandbits
from pwn import *
from Crypto.Util.number import *
c = remote('02.cr.yp.toc.tf', 17113)
# c.interactive()

for i in range(30, 30 + 19):
    c.recvuntil(f'{i}-bit:')
    c.recvline()
    z = getRandomNBitInteger(i)
    c.sendline(f'{z*z},{z*z},{z}')
    print(c.recvline())
# CCTF{4_diOpH4nT1nE_3Qua7i0n__8Y__Jekuthiel_Ginsbur!!}