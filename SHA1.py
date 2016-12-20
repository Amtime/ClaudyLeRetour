from GS15lib import left_padding, random_bytes
from CONST import INIT_H


def permut_circu(k, w):
    w = w[k:] + w[0:k-1]
    return w


def add_modulo(a,b):
    # Input strings binaire 32 bits
    # Output add modulo 2^32 sur 32 bits
    res = (int(a,2) + int(b,2)) % pow(2, 32)
    return '{0:0{1}b}'.format(res, 32)


def const_t(t):
    # Affectation de la constante K selon t
    if t in range(0,20):     res = 0x5A827999
    elif t in range(20, 40): res = 0x6ED9EBA1
    elif t in range(40, 60): res = 0xAC52C1D5
    elif t in range(60, 80): res = 0x8F1BBCDC
    else: print("Erreur"); return
    #print("Constante : ",bin(int(res, 16))[2:].zfill(32))
    return '{0:0{1}b}'.format(res, 32)


def fonc_t(t, b, c, d):
    """
    :param t: Fonction parametrique Ft
    :param b: Mot aléatoires 32 bits
    :param c: Mot aléatoires 32 bits
    :param d: Mot aléatoires 32 bits
    :return: Opération selon t sur B, C, D sur 32 bits
    """
    b, c, d = int(b, 2), int(c, 2), int(d, 2)
    if t in range(0,20):    res = (b & c) | (b & d)
    elif t in range(20, 40): res = b ^ c ^ d
    elif t in range(40, 60): res = (b & c) | (b & d) | (c & d)
    elif t in range(60, 80): res = b ^ c ^ d
    return '{0:0{1}b}'.format(res, 32)


def prep_message(x, x_array = []):
    if len(x) > pow(2, 64): return
    else: x += "1"

    while (len(x) + 64) % 512 != 0:  x += "0"

    x += left_padding(format(len(x), '010b'), "0", 64)

    for i in range(0, int(len(x)/512)): # i = 0...nBlocs512
        x_array.append(x[i*512:(i+1)*512]) # Array de 0 à ...nBlocs
    return x_array


def calcul_hash(x_array, w_array = []):
    # Init des vecteurs d'initialisation
    A = random_bytes(32)
    B = random_bytes(32)
    C = random_bytes(32)
    D = random_bytes(32)
    E = random_bytes(32)

    # Création des mots de 16x32bits pour chaque bloc de 512bits
    for xi_array in x_array:
        for i in range(0, 16):
            w_array.append(xi_array[i*32:((i+1)*32)])

    # Initialisation des Wt
    for t in range(15,80):
        operation = int(w_array[t - 3], 2) ^ int(w_array[t - 8], 2) \
            ^ int(w_array[t - 14], 2) ^ int(w_array[t - 16], 2)

        w_array.append(permut_circu(1, '{0:0{1}b}'.format(operation, 32)))
    print(w_array)

    # Calcul des T,C
    for t in range(0,80): # De 0 à 79
        print("T = ", t)
        print("Ft :        ", fonc_t(t, B, C, D))
        print("Constante : ", const_t(t), "\n")

        print(A)
        print(permut_circu(5, str(A)))

        #T = add_modulo(permut_circu(5, ))
        # 1. T = S5(A) + f(BCD) + E + Wt + Kt
        # E = D
        # D = C
        # C = S30(B)
        # B = A
        # A = T
        #res1 = add_modulo(permut_circu(5, '{0:0{1}b}'.format(A, 32)), fonc_t(t, B, C, D))
        #print(res1)

        # 2. H0 = H0 + A
        #    H1 = H1 + B
        #    H2 = H2 + C
        #    H3 = H3 + D
        #    H4 = H4 + E
        pass



def SHA1(x):
    x_array = prep_message(x)
    hash_final = calcul_hash(x_array)


def main():
    SHA1("010100101001000000001")


if __name__ == "__main__":
    main()