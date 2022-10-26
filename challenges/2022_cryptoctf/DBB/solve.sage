# y^2 = x^3 + 31337x + B
n = 34251514713797768233812437040287772542697202020425182292607025836827373815449
x, y = 10680461779722115247262931380341483368049926186118123639977587326958923276962, 4003189979292111789806553325182843073711756529590890801151565205419771496727
B = (y^2-x^3-31337*x) % n
base_x = 7331
F = IntegerModRing(n)
E = EllipticCurve(F, [31337, B])
P = E(x, y)
base_y = F(base_x^3+31337*base_x+B).sqrt()
base = E(base_x, base_y)
# factors = list(factor(n))
factors = [11522256336953175349, 14624100800238964261, 203269901862625480538481088870282608241]
modulus, moduli = [], []
for p in factors:
    F = GF(p)
#     F = IntegerModRing(n)
    curve = EllipticCurve(F, [31337, B])

    P = curve(x, y)
    base0, base1 = curve(base_x, base_y), curve(base_x, -base_y)
    for base in [base0, base1]:
        n = base.discrete_log(P)
        m = base.order()
        moduli.append(n)
        modulus.append(m)
print(modulus, moduli)
for i in range(2):
    print(long_to_bytes(crt([moduli[i], moduli[i+2], moduli[i+4]], [modulus[i], modulus[i+2], modulus[i+4]])))
# CCTF{p0Hl!9_H31LmaN_4tTackin9!}
