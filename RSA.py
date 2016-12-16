from GS15lib import identite_bezout, decoupage_string
from CONST import PRIMES
import random
from base64 import b64decode, b64encode, standard_b64decode
import codecs


def gen_cles():
    p = PRIMES[random.randint(0, len(PRIMES))]
    q = PRIMES[random.randint(0, len(PRIMES))]
    # TODO Generation nb premiers

    q_inv = 1
    while (q*q_inv)%p != 1:
        p = PRIMES[random.randint(0, len(PRIMES))]
        q = PRIMES[random.randint(0, len(PRIMES))]
        q_inv = identite_bezout(q,p)[1]

    n = p * q
    print("N : ", n)
    n_hex = hex(n)
    print("Hex_N : ", n_hex)
    print(codecs.encode(n))

    phi = (p-1)*(q-1)

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

    with open("Keys/private_key_PKCS.txt", "w") as f:
        f.write(str(d) + "\n" + str(n) + "\n" + str(p) + "\n" + str(q) + "\n" + str(q_inv) + "\n" + str(dp) + "\n" + str(dq))
    with open("Keys/public_key.txt", "w") as f:
        f.write(str(e) + "\n" + str(n))


def chiffrement(message, cle_publique):
    e, n = cle_publique
    print(message)
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


def dechiffrement(cypher, cle_secrete):
    d, n, p, q, q_inv, dp, dq = cle_secrete

    # Dechiffrement par exponentiation
    liste_dechifree1 = []
    for c in cypher:
        clair = pow(c, d) % n
        liste_dechifree1.append(chr(clair))
    messageclair1 = ''.join(liste_dechifree1)
    print(messageclair1)

    # Dechiffrement avec le TRC
    liste_dechifree2 = []
    for c in cypher:
        mp = pow(c, dp) % p
        mq = pow(c, dq) % q
        h = q_inv * (mp - mq) % p
        clair = mq + (h * q) % n
        liste_dechifree2.append(chr(clair))
    messageclair2 = ''.join(liste_dechifree2)
    print(messageclair2)


def main():
    # 1. Generation des clés
    gen_cles()

    # 2. Lecture de clés
    with open('Keys/private_key_PKCS.txt') as f:
        d, n, p, q, q_inv, dp, dq = f.readlines()
    cle_secrete = int(d), int(n), int(p), int(q), int(q_inv), int(dp), int(dq)
    with open('Keys/public_key.txt') as f:
        e, n = f.readlines()
    cle_publique = int(e), int(n)

    # 3. Chiffrement
    cypher = chiffrement("Attack at dawn", cle_publique)
    print("liste chifree :          ", cypher)

    # 4. Dechiffrement
    dechiffrement(cypher, cle_secrete)


if __name__ == "__main__":
    main()