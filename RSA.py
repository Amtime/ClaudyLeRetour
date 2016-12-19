from GS15lib import identite_bezout, decoupage_string, left_padding, random_bytes
from CONST import PRIMES_4
from base64 import b64decode, b64encode, standard_b64decode
from primegen import go_prime
import random, codecs, time, hashlib


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('%s function took %0.3f ms' % (f.__name__, (time2-time1)*1000.0))
        return ret
    return wrap


def OAEP_encode(m, em_len):
    """


    :param m: Message à chiffrer
    :param em_len: Longueur en octets du message chiffré, au moins 2*h_len + 1 : encoded message length
    :return: Message chiffré de longueur em_Len
    """
    p = random_bytes(8)
    # 1. Test de la longueur de p, ne doit pas dépasser la limite d'input de
    # la fonction de hash.

    # 2. Test de la longueur du message.
    # m_len > em_len - 2h_len - 1

    # 3. Generation d'une chaine de 0 de longueur : PS
    # em_Len - m_len - 2h_len - 1 en octets

    # 4. p_hash = Hash(p)

    # 5. Concatenation
    # DB = p_hash + PS + 01 + m

    # 6. Generation d'un octet aléatoire : seed
    # de longueur h_len

    # 7. dbMask = MGF(seed, em_len-h_len)

    # 8. maskedDB = XOR(DB, dbMask)

    # 9. seedMask = MGF(maskedDB, h_len)

    # 10. maskedSeed = XOR(seed, seedMask)

    # 11. EM = concat : maskedSeed, maskedDB
    pass


def chiffrement(message, cle_publique):
    print("\n \n -------- CHIFFREMENT --------")
    e, n = cle_publique

    print("MESSAGE : ", message)
    liste_binaire = []
    for carac in message:
        liste_binaire.append(format(ord(carac), '010b'))
    print("Message converti ASCII : ", liste_binaire)

    OAEP_encode("hey", "ho")

    liste_chif = []
    for binaire in liste_binaire:

        # Padding OAEP
        grand_n = len(bin(n)) - 2
        to_pad = format(int(ascii), 'b')
        print("\nOAEP : \nOAEP BINAIRE : ", to_pad)
        petit_a = left_padding(to_pad, "0", len(to_pad) + 10)
        print("OAEP PADDED : ", petit_a)

        petit_x = random_bytes(30)
        print("OAEP SeqAleatoire : ", petit_x)

        # HASH, on veut len(X) = len(N+a)
        test_hash = hashlib.md5()
        test_hash.update(petit_x.encode())
        grand_x = test_hash.hexdigest()
        print("Premier Hash - 128 bits : ", grand_x)

        #grand_m = XOR(petit_m -  , grand_x - 128 bits)

        # Conversion ASCII - INT
        ascii = int(ascii)

        # Exponentiation
        carac_pow = fast_exp(ascii, e, n)
        liste_chif.append(carac_pow)
    return liste_chif


def fast_exp(x,k,m):
    X = x
    E = k
    Y = 1
    while E > 0:
        if E % 2 == 0:
            X = (X * X) % m
            E = E/2
        else:
            Y = (X * Y) % m
            E = E - 1
    return Y


def lecture_prime():
    go_prime()
    print(" -------- LECTURE PREMIERS --------")
    total_lignes = sum(1 for line in open("primes.txt"))
    #num_lignes_up = int(0.75 * num_lignes)

    while True:
        rand = random.randint(int(0.90 * total_lignes), total_lignes - 4)
        with open("primes.txt", "r") as f:
            p = int(f.readlines()[rand])
        with open("primes.txt", "r") as f:
            q = int(f.readlines()[rand + 4])
        if int(p) != int(q): break

    return p, q


def gen_cles():
    print(" -------- GENERATION CLES --------")

    p, q = lecture_prime()
    q_inv = 1
    while (q*q_inv)%p != 1:
        p, q = lecture_prime()
        q_inv = identite_bezout(q,p)[1]

    print("P : ", p)
    print("Q : ", q)
    n = p * q
    print("TAILLE APPROX DE LA CLé : ", (len(bin(n))-2))
    print("N : ", n)
    phi = (p-1)*(q-1)

    while (True):
        e = random.randint(1, phi)
        d = identite_bezout(e, phi)[1]
        if e % 2 != 0:
            if identite_bezout(e, phi-1)[0] == 1:
                if (e * d) % phi == 1:
                    break

    dp = d % (p - 1)
    dq = d % (q - 1)
    print("DP : ", dp)
    print("DQ : ", dq)

    with open("Keys/private_key_PKCS.txt", "w") as f:
        f.write(str(d) + "\n" + str(n) + "\n" + str(p) + "\n" + str(q) + "\n" + str(q_inv) + "\n" + str(dp) + "\n" + str(dq))
    with open("Keys/public_key.txt", "w") as f:
        f.write(str(e) + "\n" + str(n))


def dechiffrement_exponentiation_fast(cypher, cle_secrete):
    print("\n \n -------- EXP DECHIFFREMENT fast() --------")
    d, n, p, q, q_inv, dp, dq = cle_secrete

    liste_dechifree1 = []
    for c in cypher:
        clair = fast_exp(c, d, n)
        liste_dechifree1.append(clair)
        print(clair)
    #messageclair1 = ''.join(liste_dechifree1)
    #print(messageclair1)


def dechiffrement_exponentiation_pow(cypher, cle_secrete):
    print("\n \n -------- EXP DECHIFFREMENT pow() --------")
    d, n, p, q, q_inv, dp, dq = cle_secrete

    liste_dechifree1 = []
    for c in cypher:
        clair = pow(c, d) % n
        liste_dechifree1.append(clair)
        print(clair)
    #messageclair1 = ''.join(liste_dechifree1)
    #print(messageclair1)


def dechiffrement_trc_fast(cypher, cle_secrete):
    print("\n \n -------- TRC DECHIFFREMENT fast() --------")
    d, n, p, q, q_inv, dp, dq = cle_secrete

    liste_dechifree2 = []
    for c in cypher:
        mp = fast_exp(c, dp, p)
        print("MP : ", mp)
        mq = fast_exp(c, dq, q)
        print("MQ : ", mq)
        h = (q_inv * (mp - mq + p)) % p
        print("H : ", h)
        clair = (mq + (h * q)) % n
        print("CLAIR : ", clair)
        #liste_dechifree2.append(chr(clair))
    #messageclair2 = ''.join(liste_dechifree2)
    #print(messageclair2)


def dechiffrement_trc_pow(cypher, cle_secrete):
    print("\n \n -------- TRC DECHIFFREMENT pow() --------")
    d, n, p, q, q_inv, dp, dq = cle_secrete

    liste_dechifree2 = []
    for c in cypher:
        mp = pow(c, dp) % p
        print("MP : ", mp)

        mq = pow(c, dq) % q
        print("MQ : ", mq)

        h = (q_inv * (mp - mq + p)) % p
        print("H : ", h)

        clair = (mq + (h * q)) % n
        print("CLAIR : ", clair)

        mprim = (mp - mq) * q
        print("M' : ", mprim)

        clair2 = (mprim * q_inv) + mq
        print("CLAIR2 : ", clair2)
        #liste_dechifree2.append(chr(clair))
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
    cypher = chiffrement("a", cle_publique)
    print("liste chifree :          ", cypher)

    # 4. Dechiffrement
    #dechiffrement_exponentiation_fast(cypher, cle_secrete)
    #dechiffrement_exponentiation_pow(cypher, cle_secrete)
    #dechiffrement_trc_fast(cypher, cle_secrete)
    #dechiffrement_trc_pow(cypher, cle_secrete)


if __name__ == "__main__":
    main()