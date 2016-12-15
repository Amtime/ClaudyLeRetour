from GS15lib import *
from CONST import *
import random


def cles():
    p = PRIMES[random.randint(0, len(PRIMES))]
    q = PRIMES[random.randint(0, len(PRIMES))]
    n = p*q
    q_inv = 1
    phi = (p-1)*(q-1)

    while (q*q_inv)%p != 1:
        p = PRIMES[random.randint(0, len(PRIMES))]
        q = PRIMES[random.randint(0, len(PRIMES))]
        q_inv = identite_bezout(q,p)[1]

    while (True):
        e = random.randint(1, phi)
        d = identite_bezout(e, phi)[1]
        if e % 2 != 0:
            if identite_bezout(e, phi-1)[0] == 1:
                if (e * d) % phi == 1:
                    break
            else:
                e = random.randint(1, phi-1)
        else:
            e = random.randint(1, phi-1)
    dp = d % (p - 1)
    dq = d % (q - 1)

    return e, d, n, dp, dq, p, q, q_inv


def chiffrement(message, e, n):
    liste_ascii = []
    for carac in message:
        asciicarac = ord(carac)
        liste_ascii.append(asciicarac)

    liste_ascii = [71, 83, 49, 53]
    print("liste convertie ASCII : ", liste_ascii)
    liste_chif = []
    for ascii in liste_ascii:
        ascii = int(ascii)
        carac_pow = pow(ascii, e)
        chiffre = carac_pow % n
        liste_chif.append(chiffre)
    return(liste_chif)


def dechiffrement(cypher, d, n, dp, dq, p, q, q_inv):
    liste_clair1 = []
    for c in cypher:
        clair = pow(c, d) % n
        liste_clair1.append(clair)
    print("liste clair1 : ", liste_clair1)

    liste_clair2 = []
    for c in cypher:
        mp = pow(c, dp) % p
        mq = pow(c, dq) % q
        h = q_inv * (mp - mq) % p
        clair = mq + (h * q) % n
        liste_clair2.append(clair)
    print("liste clair2 : ", liste_clair2)


def main():
    e, d, n, dp, dq, p, q, q_inv = cles()
    cypher = chiffrement("CRYPTO", e, n)
    print("liste chifree :          ", cypher)
    dechiffrement(cypher, 11787, 17947, 91, 87, 137, 131, 114)
    # cypher , d , n , dp , dq , p , q , q_inv


if __name__ == "__main__":
    main()