# ISITDTU2022 Crypto Challenge
I had a chance to play ISITDTU2022, since it is a well-known CTF with high quality challenges. This is a challenge that I find it interesting. There is another version of this challenge that I did not manage to solve during the the contest.

## Glitch in the matrix
### Problem
The problem shows 3 options: 
- Guess the password
- Yield an encrypted version of a password
- Change another password
The password is a hex representation of a 8-bytes string.

Take a look at the **encrypt** function
``` python
def encrypt(message: bytes) -> str:
    M = [b for c in message for b in map(int, "{:08b}".format(c))]
    ct = []
    for bit in M:
        C = random_bits(64)
        v = f(SECRET_BASIS[:64], C) if bit else f(SECRET_BASIS[64:], C)
        ct.extend(v)
    ct = "".join(map(str, ct))
    return bytes([int(ct[i:i+8], 2) for i in range(0, len(ct), 8)]).hex()

```
The challenge provides a ***SECRET_BASIS*** is a 128x128 matrix consists only of 0s and 1s

First the message is converted into bit string, then the algorithm iterates over the bit string, if the bit is 1 then it output the **f** with the first 64 basis with a random bit string. Otherwise it output the **f** with the last 64 basis with a random bit string.

Now take a look at the **f** function
```python
def f(M: list[list[int]], C: list[int]) -> list[int]:
    v = [0] * len(M[0])
    for c, m in zip(C, M):
        if c:
            v = [x ^ y for x, y in zip(v, m)]
    return v
```

Looks like the function f xor the basis with the bit string C as the mask.

So the task is to recover the password from the encrypted password.

### Some thought
At first I have no idea what to do, a random mask seem to be to difficult to handle. Then the term basis reminds me of vector space, and the rest comes to me naturally.

First take a look of function **f** again.
Basically, the **f** function calculates the following expression
$$f = \sum_{i=1}^{64} a_i \boldsymbol{v_i}$$

**Explanation**: Rewrite the function f, 
$$f = (a_{1} \& \boldsymbol{v_{1}}) \oplus (a_{2} \& \boldsymbol{v_{2}}) \oplus ... \oplus(a_{64} \& \boldsymbol{v_{64}}) $$

Where $a_i$ is the $i^{th}$ bit of the bit string C, and $\boldsymbol{v_i}$ is the $i^{th}$ basis of M. The operator $\&$ is the bitwise and. The operator $\oplus$ is the xor operator.

Consider these operator in **GF(2)**, the and, xor operator are equivalent to multiplication, addition operator. 

| $a$      | $b$      | $a+b$    | $a\oplus b$    | $a*b$    | $a\&b$ |
| :---:  | :---:  | :---:  | :---:  | :---:  | :---:  | 
| 0      | 0      | 0      | 0      | 0      | 0      |
| 0      | 1      | 1      | 1      | 0      | 0      |
| 1      | 0      | 1      | 1      | 0      | 0      |
| 1      | 1      | 0      | 0      | 1      | 1      |

The output of the first bit in the password is a linear combination of the 64 basis with random coefficients. Then if we have enough ciphertext, we could get 64 independent vector to form a base spanning the same subspace as the original base.

```python
def check():
    global cts

    M = ZZ^128 # Create vector of dimension 128
    C = VectorSpaces(FiniteField(2)) # Vector space on GF(2)
    t = [u[:128] for u in cts]
    W = M.submodule(t) # Subspace formed by the specified vector
    J = C(W).basis_matrix() # Convert the subspace to GF(2) and calculate the basis

    if J.nrows() == len(cts): # Number of basis 
        if len(cts) == 64:
            return True
        else:
            return False
    else: # The last vector is linear dependent on the previous vector
        cts.pop()
        return False


cts = []
while True:
    ct = convert(get_ct())
    assert len(ct) == 8192
    cts.append(ct)
    if check():
        break
```

Then for each vector, if that vector is in the subspace spanned by the original base, that bit is the same as the first bit of the password. Otherwise it is the other bit. 

To check I use the code to generate the vector space formed by the specified vectors, then used gaussian elimination to retrieve the number of basis of the subspace.

If the number of basis is 64, it implies the 65$^{th}$ vector is in that subspace. Otherwise the number of basis is 65 (the final vector is linear independent from the 64 basis)

```python
ct = cts[1]
res = ''
for i in tqdm(range(0, len(ct), 128)):
    tmp = ct[i:i+128]  
    M = ZZ^128
    C = VectorSpaces(FiniteField(2))
    t = [u[:128] for u in cts] + [tmp]
    W = M.submodule(t)
    J = C(W).basis_matrix()
    if J.nrows() == 64: # Assume the first bit is 0
        res += '0'
    else:
        res += '1'
print(res)
# Submit for case first bit is 0
submit(res)
# Submit for case first bit is 1
submit(reverse_bit(res))
# Either case must be correct
```

## Version2
Second version of the challenge add a little tweak to the encrypt function
``` python
def encrypt(message: bytes) -> str:
    M = [b for c in message for b in map(int, "{:08b}".format(c))]
    ct = []
    random.shuffle(SECRET_BASIS)
    for bit in M:
        C = random_bits(64)
        v = f(SECRET_BASIS[:64], C) if bit else f(SECRET_BASIS[64:], C)
        ct.extend(v)
    ct = "".join(map(str, ct))
    return bytes([int(ct[i:i+8], 2) for i in range(0, len(ct), 8)]).hex()

```

Since the basis is shuffled for each time the password is encrypted, I have no idea how to construct the equivalent basis

The author also released a hint: The possibility might tell you something 

**Update**: Still no idea :)