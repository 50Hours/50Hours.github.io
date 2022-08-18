import telnetlib

io = telnetlib.Telnet('05.cr.yp.toc.tf','37331')

io.read_until(b'uit\n')
io.write(b'G\n')
io.read_until(b'=')
n = int(io.read_until(b'\n'))
print(n)
# n = 2735857198516780457633636135368540426080811045093428372343321564042954049
factors = factor(n)

io.write(b'S\n')

def sq(n):
    assert is_prime(n)
    F = GF(n)
    z = int(F(-1).sqrt())
    if z > n - z:
        z = n - z
    
    thres = ceil(sqrt(n))
    r_pre, u_pre, r, u = n, n, n, z
    while True:
        if r < thres:
            break
        r_pre, u_pre, r, u = r, u, u, r % u
    return r
x, y = 0, 1
for f in factors:
    u = sq(f[0])
    v = sqrt(f[0]-u^2)
    assert u^2 + v^2 == f[0]
    x, y = x*u + y*v, x*v - y*u

assert x^2+y^2 == n
print(x, ',', y)
io.write(str(x).encode() + b',' + str(y).encode())
print(io.read(1024))