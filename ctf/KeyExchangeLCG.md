# Key Exchange Scheme using Linear Congruent Generator

**Note**:

The idea for this blog is based on the challenge Exchange in the 2022 corCTF by problem settler **willwam**

-----------

The Diffie-Hellman key exchange is a famous way for securedly establishing a shared key among two parties. The protocol is proven to be secured by the hardness of the discrete log problem.

## How original Diffie-Hellman works

Assume Alice and Bob want to establish a shared key for a symetric-key encryption (for example DES, AES, etc.. ). 

Then first both Alice and Bob agree on a big prime $p$, and a generator $g$ which is a primitive root modulo $p$. These value could be agree in plaintext (It is OK for Eve to know these value)

Alice and Bob each has a secret value $a$ and $b$.

Then Alice send to Bob $g^a$ mod $p$, and Bob send to Alice the value $g^b$ mod $p$.

As Bob receive the value of $g^a$. He could calculate the shared value $(g^a)^b = g^{ab} = (g^b)^a$. The same for Alice.

Then both of them now agree for the same value.

## Some technical notice
### Why $g$ has to be a primitive root?

In order to ensure that the shared value could take any value in range of $1$ to $p - 1$, then g must be primitive root.

### Why is it secure?
Imagine Eve is an eavesdropper and able to capture the following values: $g$, $p$, $g^a$ and $g^b$. The question is could Eve be able to effectively calculate the shared secret.

If the answer is yes, then the protocol is considered to be insecured.

Fortunately, in order to calculate the shared secret, Eve has to recovered either $a$ or $b$ from the captured information. However, it is the popular discrete log problem, which is known to be hard to solve effectively.

-----

## Could we invent another scheme using another primitive like the LCG for Diffie Hellman ??

The answer is yes. But is it secured ?? No, of course =))

Let take a look at how the scheme would look like, and how it works.

First we will take a look at definition for some of the terms

### Linear Congruent Generator (LCG)

LCG is a pseudo-random generator that yeild a sequence of number based on the following equation:

$$x_{i+1} = (a x_i + b) \text{ mod } p$$

Initially, the value of $x_0$ is considered to be the seed of the generator. Then the next random value is created based on the previous value and so on.

### So how does it fit in the DH protocol

So now assume both Alice and Bob publicly agree on the LCG and a seed, which is the value of $x_0$, $a$, $b$, and $p$. 

The term **publicly agree** means that it is ok for Eve to get that information also.

Then, both Alice and Bob have a secret value, namely $n_a$ and $n_b$.

Then Alice send to Bob the value of $A = f_{n_a}(x_0)$, where $f_{n}(x) = f(f(..f(x)))$ n times. The same for Bob.

Then both of Alice and Bob would agree on the value of 

$$f_{n_a}(f_{n_b}(x)) = f(f(..f(x)) = f_{n_b}(f_{n_a}(x))$$

Since both of them are $f(f(..f(x)))$ with $n_a+n_b$ times

So the problem remained is whether Eve could calculate the secrete value of either Bob or Alice secret value by knowing all the value transmitted among Alice and Bob.

### It's Eve time.

Suppose you are now Eve, and you want to know how to retrieve the secret value of $a$ and $b$

Let's take a look at how $f_n(x)$ looks like

$$f_1(x) = ax + b$$
$$f_2(x) = a(ax + b) + b = a^2x+ab+b$$
$$f_3(x) = a(a^2x+ab+b)+b= a^3x + a^2b+ab+b$$

So using induction, we could conclude that
$$f_n(x) = a^nx + a^{n-1}b + a^{n-2}b + ... + b$$
i.e
$$f_n(x) = a^nx + \frac{b(a^{n} - 1)}{a-1} $$

Therefore with known value of $x$, $a$ and $b$, it is possible to calculate the value of $a^n$

So if Eve could retrieve the secret value of $n_a$ from $f_{n_a}(x)$ then there is a way to retrieve $n_a$ from $x^{n_a}$ and $x$.

### Conclusion
So this is secure due to the same characteristic of the original DH protocol 

--------------------------
**Done, there is nothing left to see, and the challenge cannot be solve.**

-----------------------------------------

## Do you see the problem ??
The problem is that you already assumed that to calculate the shared value, one must retrieve the secret value of either Alice or Bob, which is not true for some cases (especially in this case).

One of the notice that would break the whole protocol is that 

$$f(x) - f(y) = a(x - y)$$
i.e
$$f(f(x)) - f(f(y)) = a(f(x)-f(y)) = a^2(x - y)$$
Therefore, by induction, we get the following result
$$f_n(x) - f_n(y) = a(f_{n-1}(x)-f_{n-1}(y)) = a(a^{n-1}(x - y)) = a^n(x-y)$$

So what if the shared secret could be calculated without knowing the value of $n_a$ or $n_b$. Denote shared secret as $ss$

$$ss = f_{n_a}(f_{n_b}(x)) = f_{n_a}(B)$$
$$ss - A = ss - f_{n_a}(x) = f_{n_a}(B) - f_{n_a}(x) = a^{n_a}(B - x)$$

With the known value of $A$, $a^{n_a}$, $B$ and $x$, one could easily calculate the shared secret between Alice and Bob easily, hence break the confidentiality of the communication.