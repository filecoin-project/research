# VDF Attack 1: SPLITZY ATTACK

Author: Brian Vohaska

----

As discussed at Team Week, here is the outline of a pretty simple possible cryptographic attack on VDF-RSA. This attack is for a _very very_ special case that we expect to see in practice with probability very close to cryptographic-zero. Nevertheless, this attack should be looked at to ensure that it can't be generalized.

Note to those reading this: sorry about the error. No LaTex here so I'm winging it with the markdown. Feel free to correct variable/index issues.

## SPLITZY Attack

*ExecuSummary: We make exponentiation faster and compute VDF faster than others. [Time-Space Trade-Offs](https://en.wikipedia.org/wiki/Space%E2%80%93time_tradeoff).*

This attack assumes modular exponentiation on an RSA group with a slowly changing modulus. The goal of this attack is to compute a series of modular exponentiations faster than an honest actor. Where the only advantage an honest actor will implement is [square and multiply](https://en.wikipedia.org/wiki/Exponentiation_by_squaring). The following are assumptions we make about the VDF system,

1. `N = p*q` where `p`,`q` are primes
2. `j` is a _m-bit smooth integer_ chosen at random
3. `T` is a very large integer and is publicly known

VDF is of the form,

`j^(2^T) (mod N)`

### One-time Step

#### Step 1

For all m-bit primes `I : prime_i in Z/N` compute,

    `c = i^2^T (mod N)` 

and store the result in a table we call `C`. This results in a storage requirement of about `(m*log(n))/log(m)` bits. For a more precise calculation use the prime density theorem and associated lemmata.

#### Step 2

Given that `j` is chosen from `Z/N`, calculate the prime factorization for `y` m-bit smooth integers,

    `y = {r_0, r_1, ... , r_y-1}`

    `E = {e_m} <-- Factor(r_w) = p_0^e_0 * p_1^e_1 * ... * p_m^e_m` 

for all `0 <= w < y`

Using a chosen average, calculate the most likely set `E` for a given m-bit smooth integer in `Z/N`

For all `e_i in E` and `c in C` calculate and store

    `u = c^(e_i - x)`

where `x` is an integer chosen based on prime density theorem and ensures that `u` will be close to a desired factorization in Step 2 of this attack. The storage requirement is on the order of `|C|`.

(optionally) store for a set `u = c^(e_i - x)` for various choices of `x`.

### Every-time Step

Factor `j`,

`j = p_0^e_0 * p_1^e_1 * ... * p_m^e_m` where p_i is m-bit smooth

Recall out VDF,

    j^(2^T) (mod N)

    (p_0^e_0 * p_1^e_1 * ... * p_m^e_m)^2^T (mod N)

    (p_0^e_0)^2^T * (p_1^e_1)^2^T * ... * (p_m^e_m)^2^T (mod N)

Note that we have stored `p0_2T = (p_0^e_0)^2^T (mod N)` as well as integers close to `p0_2T`. Since `mod N` is linear we have,

    (p_0^e_0)^2^T (mod N) * (p_1^e_1)^2^T (mod N) * ... * (p_m^e_m)^2^T (mod N) (mod N)

    (p0_2T) * (p1_2T) * ... * (pm_2T) (mod N)

Suppose `m|d = 4` for some integer `d` then,

    P1 = (p0_2T) * (p1_2T) * ... * (p(m/4)_2T)

    ....

    P4 = (p(3m/4)_2T) * ... * (pm_2T) (mod N)

Each part can be computed in parallel and combined later,

    VDF = P1 * ... * P4 (mod N)

### Trivial Examples

####  Suppose `j = (2^18236213)`, log(N) = 2048

It happens that `log(18236213) = 25` thus`j` is 25-bit smooth. Furthermore, _for reasons_ all choices of `j` will be 26-bit smooth. Therefore we need to store about (2^26)*2048/26 bits = 630 MB in our pre-compute table or about 1GB if we want to allow for some wiggle room for our choices of `c`.

Now we need to compute the VDF,

    VDF = j^2^T = (2^18236213)^2^T (mod N)

         = (2^2^T)^18236213 = (2^2^T)^(e_2 - x) = (2^2^T)^(e_2) / (2^2^T)^(x) (mod N)

where `x << T` be our choices of `c`

        = (c_2) * (p2_2T)^x

we calculate `(p2_2T)^x` which is very easy since we have precomputed `p2_2T` and `x << T`.

#### Suppose `j` = (2^2134347) * (13^2138097)

Again, _for reasons_ all choices of `j` will be 26-bit smooth. Thus, we need about `GB to store our precompute table.

Now we need to compute the VDF,

    VDF = j^2^T = ((2^2134347) * (13^2138097))^2^T (mod N)

        = (2^2^T)^2134347 * (13^2^T)^2138097 (mod N)

        = (2^2^T)^(e_2 - x) * (13^2^T)^(e_13 - x) (mod N)

        = (2^2^T)^(e_2 ) / (2^2^T)^(x) * (13^2^T)^(e_13 - x) / (13^2^T)^(x) (mod N)

        = c_2 * (p2_2T)^x * c_13 * (p13_2T)^x

where `x << T` be our choices of `c`

we calculate `(p2_2T)^x` and (p13_2T)^x  which is very easy since we have precomputed `p2_2T`, `(p13_2T)`,  and `x << T`.

### Mitigations

Probably not needed at this point since this attack relies on unlikely events. However, it might be prudent to consider other VDF constructions If the attack can be generalized.
