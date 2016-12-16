from GS15lib import identite_bezout, decoupage_string
from CONST import PRIMES_20
import random
from base64 import b64decode, b64encode, standard_b64decode
import codecs
import time


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('%s function took %0.3f ms' % (f.__name__, (time2-time1)*1000.0))
        return ret
    return wrap


def fast_exp(x,e,m):
    X = x
    E = e
    Y = 1
    while E > 0:
        if E % 2 == 0:
            X = (X * X) % m
            E = E/2
        else:
            Y = (X * Y) % m
            E = E - 1
    return Y


def gen_cles():
    p = PRIMES_20[random.randint(0, len(PRIMES_20)-1)]
    q = PRIMES_20[random.randint(0, len(PRIMES_20)-1)]
    # TODO Generation nb premiers

    q_inv = 1
    while (q*q_inv)%p != 1:
        p = PRIMES_20[random.randint(0, len(PRIMES_20)-1)]
        q = PRIMES_20[random.randint(0, len(PRIMES_20)-1)]
        q_inv = identite_bezout(q,p)[1]

    n = p * q
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

#@timing
def chiffrement(message, cle_publique):
    e, n = cle_publique
    print(n)
    print(message)
    liste_ascii = []
    for carac in message:
        asciicarac = ord(carac)
        liste_ascii.append(asciicarac)

    print("liste convertie ASCII : ", liste_ascii)
    liste_chif = []
    for ascii in liste_ascii:
        ascii = int(ascii)
        #carac_pow = fast_exp(ascii, e, n)
        #print(carac_pow)
        carac_pow = pow(ascii, e)
        chiffre = carac_pow % n
        print(chiffre)
        liste_chif.append(chiffre)
    return liste_chif


#@timing
def dechiffrement_exponentiation(cypher, cle_secrete):
    d, n, p, q, q_inv, dp, dq = cle_secrete

    liste_dechifree1 = []
    for c in cypher:
        clair = fast_exp(c, d, n)
        liste_dechifree1.append(chr(clair))
    messageclair1 = ''.join(liste_dechifree1)
    print(messageclair1)


#@timing
def dechiffrement_trc(cypher, cle_secrete):
    d, n, p, q, q_inv, dp, dq = cle_secrete

    liste_dechifree2 = []
    for c in cypher:
        mp = fast_exp(c, dp, p)
        mq = fast_exp(c, dq, q)
        h = q_inv * (mp - mq) % p
        clair = mq + (h * q) % n
        print(clair)
        #liste_dechifree2.append(chr(clair))
    messageclair2 = ''.join(liste_dechifree2)
    print(messageclair2)


def main():
    # 1. Generation des clés
    gen_cles()

    # 2. Lecture de clés
    with open('Keys/private_key_PKCS.txt') as f:
        d, n, p, q, q_inv, dp, dq = f.readlines()
    cle_secrete = long(d), long(n), long(p), long(q), long(q_inv), long(dp), long(dq)
    with open('Keys/public_key.txt') as f:
        e, n = f.readlines()
    cle_publique = long(e), long(n)

    # 3. Chiffrement
    cypher = chiffrement("mega secret", cle_publique)
    print("liste chifree :          ", cypher)

    # 4. Dechiffrement
    #dechiffrement_exponentiation(cypher, cle_secrete)
    dechiffrement_trc(cypher, cle_secrete)


if __name__ == "__main__":
    main()