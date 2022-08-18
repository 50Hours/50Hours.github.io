import telnetlib

io = telnetlib.Telnet('08.cr.yp.toc.tf','37313')

for _ in range(12):
    io.read_until(b'p = ')
    p = int(io.read_until(b',')[:-1])
    io.read_until(b'M = \n')

    mat = []

    content = io.read_until(b'\n').strip()[1:-1].decode().split(' ')
    content = [a for a in content if a != '']
    print(content)

    row = list(map(int, content))
    mat.append(row)

    for i in range(len(row) - 1):
        content = io.read_until(b'\n').strip()[1:-1].decode().split(' ')
        content = [a for a in content if a != '']
        print(content)

        row = list(map(int, content))
        mat.append(row)

    M = Matrix(GF(p), mat)
    order = M.multiplicative_order()
    io.read_until(b'\n')
    io.write(str(order).encode() + b'\n')
    print(io.read_until(b'\n'))
# CCTF{ma7RicES_4R3_u5EfuL_1n_PUbl!c-k3y_CrYpt0gr4Phy!}