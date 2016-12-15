from GS15lib import *
from CONST import *
import random


def cles():
    p = PRIMES[random.randint(0, len(PRIMES))]
    q = PRIMES[random.randint(0, len(PRIMES))]
    n = p*q
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
    return e, d, n


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


def dechiffrement(cypher, d, n):
    liste_clair1 = []
    for c in cypher:
        clair = pow(c, d) % n
        liste_clair1.append(clair)
    return(liste_clair1)

    liste_clair2 = []
    dp = d % (p - 1)
    dq = d % (q - 1)
    for c in cypher:
        m1 = pow(c, dp) % p
        m2 = pow(c, dq) % q
        h = (q_inv * (m1 - m2)) % p
        print("H: ", h)
        print("m1-m2: ", m1 - m2)
        # Ajout p pour garder la somme positive
        clair = m2 + (h * q)
        liste_dechif.append(chr(clair))



def main():
    e, d, n = cles()
    cypher = chiffrement("CRYPTO", e, n)
    print("liste chifree :          ", cypher)
    print("liste clair :            ", dechiffrement(cypher, d, n))


if __name__ == "__main__":
    main()