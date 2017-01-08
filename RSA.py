from GS15lib import identite_bezout, decoupage_string, left_padding, right_padding, random_bytes, XOR
from CONST import PRIMES_110
from primegen import go_prime
import random, time
from SHA1 import SHA1


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('%s function took %0.3f ms' % (f.__name__, (time2-time1)*1000.0))
        return ret
    return wrap


def OAEP_encode(N):
    #print("\n -------- PADDING OAEP --------")

    long_message = len(N)
    concat = N + right_padding("", "0", 160-len(N))  # Concat = NbitsMessage + Padding (l_padding = h_len - N)
    x = random_bytes(8)
    X = SHA1(x)
    M = XOR(concat, X)
    z = XOR(x, SHA1(M))
    return M, z, long_message


def OAEP_decode(M, z):
    # Input : Message M, chaine z

    x = XOR(SHA1(M), z)
    m = XOR(M, SHA1(x))
    return m


def chiffrement(message, path):
    print("\n \n -------- CHIFFREMENT --------")

    with open(path) as f:
        e, n, x1, x2, x3, x4, x5 = f.readlines()
    e = int(e); n = int(n)

    if len(message) % 2 != 0: message += " "
    print("Longueur message : ", len(message))
    print("MESSAGE : ", message)

    liste_binaire = []
    for carac in message: # Conversion binaire de chaque caractère >> 8 bits
        liste_binaire.append('{0:0{1}b}'.format(ord(carac), 8))
    print("Message converti ASCII : ", len(liste_binaire), liste_binaire)
    print("\nPadding de chaque ASCII en 20 blocs de 8 bits..")

    # Padding OAEP : 160 bits soit 20 fois 8bits
    liste_bin_OAEP = []
    for binaire in liste_binaire:
        M, z, l = OAEP_encode(binaire)
        for j in range(0, 20):
            liste_bin_OAEP.append(M[8 * j:8 * (j + 1)])
        for j in range(0, 20):
            liste_bin_OAEP.append(z[8 * j:8 * (j + 1)])
    print("Liste apres OAEP : ", len(liste_bin_OAEP), liste_bin_OAEP)

    # Transformation de liste_binaire en blocs de 8 bits
    liste_ent = [] # Décimaux (convertis depuis 2x8bits)
    for i in range(0, int(len(liste_bin_OAEP)/2)):
        concat_ent = liste_bin_OAEP[2*i] + liste_bin_OAEP[2*i + 1] # Concatenation par 2
        liste_ent.append(int(concat_ent, 2))       # Conversion en décimal
    print("\nRegroupement en blocs de 16bits et conversion binaire vers décimal..")
    print("Liste d'entiers : ", len(liste_ent), liste_ent)

    liste_chif = []
    for ent in liste_ent:
        exp_chif = pow(ent, e, n)
        hexa_chif = '{0:0{1}x}'.format(exp_chif, len(hex(n))-2)
        liste_chif.append(hexa_chif)                   # Longueur chif : N en hexa
    print("\nChiffrement des entiers avec la clé fournie..")
    print("Liste chifree :       ", len(liste_chif), liste_chif)

    # Ecriture du message chiffré dans un fichier
    f = open('RSA-Cypher-Output.txt', 'w')
    for c in liste_chif:
        f.write("%s\n" % c)

    return liste_chif


def dechiffrement(path):
    print("\n \n -------- DECHIFFREMENT --------")
    # Input : Liste chifree (Hexa)
    #         Cle secrete
    with open(path) as f:
        d, n, p, q, q_inv, dp, dq = f.readlines()
    d = int(d);n = int(n);p = int(p);q = int(q);q_inv = int(q_inv);dp = int(dp);dq = int(dq)


    cypher = [line.strip() for line in open("RSA-Cypher-Output.txt", 'r')]
    print("CYPHER : ", cypher)

    #1 OK Dechiffrement avec clé privée > Liste d'entiers
    print("\nDechiffrement Exponentiation et clé dérivées..")
    liste_dechifree = []
    for c in cypher:
        mp = pow(int(c, 16), dp, p)
        mq = pow(int(c, 16), dq, q)
        h = (q_inv * (mp - mq + p)) % p
        clair = (mq + (h * q)) % n
        liste_dechifree.append(clair)
    print("Liste d'entiers : ", len(liste_dechifree), liste_dechifree)

    #2 Conversion des entiers en blocs de 16 bits
    print("\nConversion chiffré > Bloc 16 bits > Blocs 8 bits..")
    liste_blocs, liste_huit = [], []
    for dechif in liste_dechifree:
        liste_blocs.append('{0:0{1}b}'.format(dechif, 16))
    print("Blocs 16 bits : ", len(liste_blocs), liste_blocs)
    #3 Séparation en blocs de 8 bits
    for bloc in liste_blocs:
        liste_huit.append(bloc[0:8])
        liste_huit.append(bloc[8:16])
    print("Blocs 8 bits : ", len(liste_huit), liste_huit)

    #4 OAEP Decode - Regroupe 20 x 8b
    print("\nRegroupement en 20x8..")
    liste_OAEP_decode = []
    for blocs in range(0, int(len(liste_huit) / 20)):
        oaep = ""
        for vin in range(0, 20):
            oaep += liste_huit[blocs*20 + vin]
        liste_OAEP_decode.append(oaep)
    print("Blocs 160 bits : ", len(liste_OAEP_decode), liste_OAEP_decode)

    print("\nSéparation des blocs Z..")
    liste_message, liste_z = [], []
    for i in range(0, int(len(liste_OAEP_decode)/2)):
        liste_message.append(liste_OAEP_decode[2*i])
        liste_z.append(liste_OAEP_decode[2*i + 1])
    print("Listes M: ", len(liste_message), liste_message)
    print("Listes z: ", len(liste_z), liste_z)

    print("\nDécodage OAEP..")
    liste_OAEP_decode = []
    for i in range(0, len(liste_message)):
        clair = OAEP_decode(liste_message[i], liste_z[i])
        liste_OAEP_decode.append(clair[0:8])
    print("Listes clair avec padding: ", len(liste_OAEP_decode), liste_OAEP_decode)

    #6 Conversion Binaire > ASCII > Caractère
    liste_clair = []
    for decod in liste_OAEP_decode:
        liste_clair.append(chr(int(decod, 2)))
    clairFinal = ''.join(liste_clair)

    print("Texte clair : ", clairFinal)
    with open("RSA-Clear-Output.txt", "w") as f:
        f.write(str(clairFinal))


def lecture_gen():
    go_prime()
    print(" -------- LECTURE PREMIERS --------")
    total_lignes = sum(1 for line in open("primes2.txt"))
    print("total ligne fichier primes : ", total_lignes)

    while True:
        rand = random.randint(1, int(total_lignes) - 3)
        print(rand)
        with open("primes2.txt", "r") as f:
            p = int(f.readlines()[rand])
        with open("primes2.txt", "r") as f:
            q = int(f.readlines()[rand + 2])
        if int(p) != int(q): break

    return p, q


def lecture_const():
    print(" -------- LECTURE PREMIERS DANS LISTE --------")
    a = random.randint(1, len(PRIMES_110)-1)
    b = random.randint(1, len(PRIMES_110)-1)

    return PRIMES_110[a], PRIMES_110[b]


def gen_cles():
    print(" -------- GENERATION CLES --------")

    p, q = lecture_const()
    q_inv = 1
    while (q*q_inv)%p != 1:
        p, q = lecture_const()
        q_inv = identite_bezout(q,p)[1]

    print("P : ", p)
    print("Q : ", q)
    n = p * q
    print("TAILLE APPROX DE LA CLé : ", (len(bin(n))-2), "BITS")
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
        f.write(str(e) + "\n" + str(n) + "\n" + "pad" + "\n" + "pad" + "\n" + "pad" + "\n" + "pad" + "\n" + "pad")


def gen_signature(message, cle_secrete):
# Generation d'une signature RSA
# Out : Message & Chiffré du message
    print("\n -------- Generation de la signature --------")

    # Lecture de D et N
    d, n, p, q, q_inv, dp, dq = cle_secrete

    # Hash du message
    hashTest = SHA1(message)

    # Chiffrement avec clé privée
    signList = []
    for i in range(0, 20):
        octet = hashTest[8 * i:8 * (i + 1)]
        cypher = pow(int(octet, 2), d, n)
        signList.append(hex(cypher))
    signString = ''.join(signList)

    print("Signature : ", signString)

    # Ecriture de la signature dans un fichier
    with open("signature.txt", "w") as f:
        f.write(str(message) + "\n" + str(signString))


def check_signature(cle_publique):
    print("\n -------- Verification de la signature --------")

    # Lecture de la clé
    e, n, x1, x2, x3, x4, x5 = cle_publique

    #with open('signature.txt') as f:
    #    message, signature = f.readlines()
    sign = [line.strip() for line in open("signature.txt", 'r')]

    # Raise signature to power E mod N
    hexList = sign[1][2:].split('0x')

    octetList = []
    for i in range(0, len(hexList)):
        entier = int(hexList[i], 16)
        decypher = pow(entier, e, n)
        octetList.append('{0:0{1}b}'.format(decypher, 8))
    hashString = ''.join(octetList)

    # Comparer les hash
    hashTest = SHA1(str(sign[0]))
    print(hashString == hashTest)

    return


def main():
        # 1. Generation des clés
        gen_cles()

        # 2. Lecture de clés
        with open('Keys/private_key_PKCS.txt') as f:
            d, n, p, q, q_inv, dp, dq = f.readlines()
        cle_secrete = int(d), int(n), int(p), int(q), int(q_inv), int(dp), int(dq)
        with open('Keys/public_key.txt') as f:
            e, n, x1, x2, x3, x4, x5 = f.readlines()
        cle_publique = int(e), int(n), x1, x2, x3, x4, x5

        # 3. Chiffrement
        chiffrement("message test", 'Keys/public_key.txt')

        # 4. Dechiffrement
        dechiffrement('Keys/private_key_PKCS.txt')

        # 5. Génération d'une signature
        gen_signature("01001101001", cle_secrete)
        check_signature(cle_publique)

if __name__ == "__main__":
    main()
