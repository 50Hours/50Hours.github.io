from itertools import product
from Crypto.Util.number import *
from string import printable

def find_prefix(a, b):
    res = 0
    for u, v in zip(a, b):
        if u != v:
            return res
        else:
            res += 1
    return min(len(a), len(b))

alphabet = (printable[:62] + "_!}").encode()
n = 23087202318856030774680571525957068827041569782431397956837104908189620961469336659300387982516148407611623358654041246574100274275974799587138270853364165853708786079644741407579091918180874935364024818882648063256767259283714592098555858095373381673229188828791636142379379969143042636324982275996627729079
c = 3621516728616736303019716820373078604485184090642291670706733720518953475684497936351864366709813094154736213978864841551795776449242009307288704109630747654430068522939150168228783644831299534766861590666590062361030323441362406214182358585821009335369275098938212859113101297279381840308568293108965668609


def check(u, v, i):
    st = u + v
    p = bytes_to_long(st)
    q = bytes_to_long(st[::-1])
    n_check = p * q
    # print(n % (256 ** (i+1)), n_check % (256 ** (i+1)))
    # print(n // (256 ** (127 - i)), n_check // (256 ** (127 - i)))
    if n % (256 ** (i+1)) == n_check % (256 ** (i+1)) \
        and n // (256 ** (127 - i)) >= n_check // (256 ** (127 - i)):
        return True
    return False

# pre, post = b'CCTF{it_is_fake_flag_', b'_90OD_luCk___!!}'
pre, post = b'', b''
pre = pre[:len(post)]
pairs = list(product(alphabet, alphabet))
print(len(pairs))

for i in range(len(pre), 32):
    print(f'Trying {i}')
    assert len(pre) == len(post)
    for u, v in pairs:
        check_pre, check_post = (pre + chr(u).encode() * 32)[:32], (chr(v).encode() * 32 + post)[-32:]
        if check(check_pre, check_post, i):
            pre += chr(u).encode()
            post = chr(v).encode() + post
            break
    print(pre, post)

# print(check((b'CCT' + b'F'*32)[:32], (b'_'*32 + b'!!}')[-32:], 3))