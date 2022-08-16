from pwn import *

# Just function for reading socket
def getParam():
    c.sendline('G')
    c.recvuntil('=')
    q = int(c.recvline())
    c.recvuntil('=')
    r = int(c.recvline())
    c.recvuntil('=')
    s = int(c.recvline())
    c.recvuntil('uit')
    c.recvline()
    return (q,r,s)

def getLen():
    try:
        content = c.recvline().decode()
        regex = re.search('([xy]) is ([0-9]+)\-bit', content)
        return regex.group(1), int(regex.group(2))
    except:
        log.success(content)
#############################################
def xgcd(a,b, x, y):
    if a < x:
        a, b, x, y = x, y, a, b
    while (x >= 2 ** 12): # Optimal threshold which is 12-bit
        k = a // x
        a, b, x, y = x, y, a % x, (b - k * y) % q
    return x, y
c = remote('04.cr.yp.toc.tf', 13777)
c.recvuntil('uit')
c.recvline()

q, r, s = getParam()

opt_x, base_y = xgcd(r, s, q, q)
opt_y, base_x = xgcd(s, r, q, q) # Notice optimal value is return first


c.sendline('S')
for _ in range(5):
    var, len = getLen()
    log.info(var + ' ' + str(len))
    # Padding the optimal value to the correct number of bits
    if var == 'x':
        bit = len - opt_x.bit_length() 
        x, y = opt_x * (2**bit), (base_y * (2 ** bit)) % q
    else:
        bit = len - opt_y.bit_length()
        x, y = (base_x * (2**bit)) % q, int((opt_y * (2 ** bit))) 
    c.sendline(str(x) + ',' + str(y))
    print(c.recvline())
# CCTF{f1nDin9_In7Eg3R_50Lut1Ons_iZ_in73rEStIn9!}