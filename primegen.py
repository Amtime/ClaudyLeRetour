import math, os.path


def test_file():
    if os.path.exists("primes2.txt"):
        with open("primes2.txt", "rb") as f: last = int(f.readlines()[-1].decode())
        return last
    else:
        with open("primes2.txt", "w") as f: f.write("Liste nombres premiers : \n")
        return 3


def sup_ligne():
    # Suppression de la premiere ligne à l'ajout d'un nouveau premier
    # Taille de fichier constant
    with open('primes2.txt', 'r') as fin:
        data = fin.read().splitlines(True)
    with open('primes2.txt', 'w') as out:
        out.writelines(data[1:])


def prime_gen(start):
    nb_test = start; nb_trouves = 0
    while True:
        is_prime = True
        for x in range(2, int(math.sqrt(nb_test) + 1)):
            if nb_test % x == 0:
                is_prime = False; break
        if is_prime:
            with open("primes2.txt", "a") as f:
                f.write("\n" + str(nb_test))
            # Suppression de la premiere ligne
            sup_ligne()
            nb_trouves += 1
            print(nb_test)
        nb_test += 1
        if nb_trouves == 100: break


def go_prime():
    start = test_file()
    prime_gen(start)


if __name__ == "__main__":
    go_prime()


def OAEP_encode(m, em_len):
    """
    :param m: Message à chiffrer, binaire
    :param em_len: Longueur en octets du message chiffré, au moins 2*h_len + 1 : encoded message length
    :return: Message chiffré de longueur em_len
    """
    m_len = len(m)
    h_len = 160  # Output SHA1
    em_len = 2 * h_len + 1  # Au moins

    # 1. Test de la longueur de p, ne doit pas dépasser la limite d'input de
    # la fonction de hash.
    if len(m) > pow(2, 64):
        print("Erreur")
        return
    else:
        print("step 1")
        pass

    # 2. Test de la longueur du message.
    # m_len > em_len - 2h_len - 1
    if m_len > em_len - 2 * h_len - 1:
        print("message trop long")
        return
    else:
        print("step 2")
        pass

    # 3. Generation d'une chaine de 0 de longueur : PS
    # em_Len - m_len - 2h_len - 1 en octets
    PS = left_padding("", 0, em_len - m_len - 2 * h_len - 1)
    print(PS)

    # 4. p_hash = Hash(p)
    p_hash = SHA1(p)
    print(p_hash)

    # 5. Concatenation
    # DB = p_hash + PS + 01 + m
    DB = str(p_hash) + PS + "01" + m

    # 6. Generation d'un octet aléatoire : seed
    # de longueur h_len
    seed = random_bytes(h_len)

    # 7. dbMask = MGF(seed, em_len-h_len)

    # 8. maskedDB = XOR(DB, dbMask)

    # 9. seedMask = MGF(maskedDB, h_len)

    # 10. maskedSeed = XOR(seed, seedMask)

    # 11. EM = concat : maskedSeed, maskedDB
    pass