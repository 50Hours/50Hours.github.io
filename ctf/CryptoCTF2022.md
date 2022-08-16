# CryptoCTF write up

This year I have not got a chance to compete in the CTF live. So I decided to up solve the challenges this year. Hopefully, the result is not too bad

Here are the challenge that I solved and the solve script (if I am not too lazy).

For each folder, the solver.py file is the solver script, all of the other files are attached file in the challenge. 


| Challenge | Difficulties | Solves | Scores |
| --------- | ------------ | -------| -------| 
| Baphomet  | easy         | 93     | 56     | 
| Klamkin   | easy         | 83     | 61     | 


# Baphomet
The scheme first encode the flag using some kind of invertible operations (base64 encoding, inverse uppercase and lowercase). Finally the flag is xored with the key derived from the flag it self. What should be notice is the length of the flag (48 characters) and the length of the key, which is $len(flag) / 8 = 6$

This challenge is a basic xor cipher with known plaintext. The known plaintext is actually the format of the flag **CCTF{**, which is 5 characters in length. But the key is derived from the base64 encoded version of the flag, which means the first $5 / 3 * 4 = 6.333$ chars is known, which is just enought to recover the key.

After that just reverse all the process with the derived key to get the flag. The solver script could be found [here](../challenges/2022_cryptoctf/baphomet/solver.py)

# Klamkin
I did not understand the challenge at first for being bad at English :((((

## Challenge
Basically, you are given a diophantine equation with given $r, s$ and $q$
$$ar + bs = 0 \text{ (mod } q \text{)}$$

Then for all pair $(a, b)$ that satisfied the above equation, we need to find 2 coefficients $(x, y)$ such that
$$ax + by = 0 \text{ (mod } q \text{)}$$
with a constraint on the magnitude of $x, y$ depending on the requirement. Most of them is in the type of $x$ or $y$ is a $k$-bit number (where $k>12$)

## Solution
The idea is to use the same algorithm as the Euclidean algorithm to find the GCD of 2 numbers. So why ??

First notice besides the equation of form $$ar + bs = 0 \text{ (mod } q \text{)}$$, there is another trivial equation that is always true, which is $$aq + bq = 0 \text{ (mod } q \text{)}$$

Then 
$$a(q-s) + b(q-r) = 0 \text{ mod } q$$

Another stronger implication is 
$$a(q-ks) + b(q-kr) = 0 \text{ mod } q$$

Hence the coefficients for a could be reduce into a small enough value. Then for each query, the only thing needed to do is to multiply that coefficient to the appropriate value.

The solver script is [here](../challenges/2022_cryptoctf/klamkin/solver.py)

