from GS15lib import left_padding, random_bytes


def permut_circu(k, w):
    w = w[k-1:] + w[0:k-1]
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
    h0 = A = "00100010111111000111100011001000"
    h1 = B = "01001110111000011110111001100001"
    h2 = C = "10011101011101000111001111100010"
    h3 = D = "00100101001000001100111100100001"
    h4 = E = "00000100100110011000000110100101"

    # Création des mots de 16x32bits pour chaque bloc de 512bits
    for xi_array in x_array:
        for i in range(0, 16):
            w_array.append(xi_array[i*32:((i+1)*32)])

    # Initialisation des Wt
    for t in range(15,80):
        operation = int(w_array[t - 3], 2) ^ int(w_array[t - 8], 2) \
            ^ int(w_array[t - 14], 2) ^ int(w_array[t - 16], 2)

        w_array.append(permut_circu(1, '{0:0{1}b}'.format(operation, 32)))

    # Calcul des T,C
    for t in range(0,80): # De 0 à 79
        grand_t = add_modulo(permut_circu(5, str(A)), fonc_t(t, B, C, D))
        grand_t = add_modulo(grand_t, E)
        grand_t = add_modulo(grand_t, w_array[t])
        grand_t = add_modulo(grand_t, const_t(t))

        E = D; D = C
        C = permut_circu(30, str(B))
        B = A; A = grand_t

    # Affectation des variables finales
    h0 = add_modulo(h0, A)
    h1 = add_modulo(h1, B)
    h2 = add_modulo(h2, C)
    h3 = add_modulo(h3, D)
    h4 = add_modulo(h4, E)

    return h0 + h1 + h2 + h3 + h4


def SHA1(x):
    # Input     : x en binaire
    # Output    : Hash SHA1 en binaire

    # Préparation du message
    x_array = prep_message(x)

    # Calcul du Hash
    final_hash = calcul_hash(x_array)

    return final_hash


def main():
    x = "0001001001001110111000100010101101001111111100101101011010111110001101010111001010000101001000010010110000001111110100111100111110011100110000001000011100111000"
    X = SHA1(x)
    print(X)
    print(SHA1(x))
    pass

if __name__ == "__main__":
    main()