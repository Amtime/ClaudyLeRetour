from GS15lib import identite_bezout
from CONST import PRIMES
import random


def cles():
    p = PRIMES[random.randint(0, len(PRIMES))]
    q = PRIMES[random.randint(0, len(PRIMES))]
    # TODO Generation nb premiers
    q_inv = 1
    while (q*q_inv)%p != 1:
        p = PRIMES[random.randint(0, len(PRIMES))]
        q = PRIMES[random.randint(0, len(PRIMES))]
        q_inv = identite_bezout(q,p)[1]
        # TODO Condition ternaire

    n = p * q
    phi = (p - 1) * (q - 1)

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

    print("liste convertie ASCII : ", liste_ascii)
    liste_chif = []
    for ascii in liste_ascii:
        ascii = int(ascii)
        carac_pow = pow(ascii, e)
        chiffre = carac_pow % n
        liste_chif.append(chiffre)
    return(liste_chif)


def dechiffrement(cypher, d, n, dp, dq, p, q, q_inv):
    # Dechiffrement par exponentiation
    liste_dechifree1 = []
    for c in cypher:
        clair = pow(c, d) % n
        liste_dechifree1.append(chr(clair))
    print("liste clair1 : ", liste_dechifree1)

    # Dechiffrement avec le TRC
    liste_dechifree2 = []
    for c in cypher:
        mp = pow(c, dp) % p
        mq = pow(c, dq) % q
        h = q_inv * (mp - mq) % p
        clair = mq + (h * q) % n
        liste_dechifree2.append(chr(clair))
    print("liste clair2 : ", liste_dechifree2)


def main():
    e, d, n, dp, dq, p, q, q_inv = cles()
    cypher = chiffrement("Chaine de caractère genre archi longue", e, n)
    print("liste chifree :          ", cypher)
    dechiffrement(cypher, d, n, dp, dq, p, q, q_inv)
    # liste chiffree cypher , d , n , dp , dq , p , q , q_inv


if __name__ == "__main__":
    main()