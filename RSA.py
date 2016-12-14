from GS15lib import *
from CONST import *

import random

""" 1. Generation des cles
    2. Ecriture des clés vers fichier
    3. Chiffrement utilisant clé publique
    4. Déchiffrement avec clé privée
    5. Générer une signature avec clé privée
    6. Vérifier signature avec clé publique
    7. RSA avec padding PKCS
"""

liste_chif = []
liste_dechif = []

def gen_keys():
    """
    Génère les fichiers de clé :
        - public_key.txt avec N, E
        - private_key_PKCS.txt avec p, q, Dp, Dq
    """

    # p et q :
    # - Premiers
    # - PGCD(p-1, q-1) = 2
    test_pq_trc = 1
    while(test_pq_trc != 2):
        p = PRIMES[random.randint(0, len(PRIMES))]
        q = PRIMES[random.randint(0, len(PRIMES))]
        test_pq_trc = identite_bezout(p-1,q-1)[0]
        print(test_pq_trc)

    # Choix de Dp et Dq entiers aléatoires TQ :
    #   - PGCD(Dp, p−1) = 1
    #   - PGCD(Dq, p−1) = 1
    #   - Dp congru à Dq modulo 2
    test_trc = 0
    while(test_trc < 2):
        test_trc = 0
        Dq = random.randint(2, 200)
        Dp = 2*random.randint(2, 200) + Dq
        if(identite_bezout(Dp, p-1)[0]):
            test_trc += 1
        if(identite_bezout(Dp, p - 1)[0]):
            test_trc += 1
        print("ESSAI")


    # Calcul de la clé D à partir des parametres PKCS
    #   D == Dp mod (p-1)
    #   D == Dq mod (q-1)
    #    > Equation reste chinois

    m = (p-1, q-1, 1)
    a = (Dp, Dq, 1)
    # Calcul de la clé privée
    D = reste_chinois(m, a)

    # Calcul de la clé publique / Chiffrement
    N = p * q
    E = identite_bezout(int(D),N)[1]

    # W:Clé publique : N, E
    # W:Clé privée : p, q, Dp, Dq
    with open("Keys/private_key_PKCS.txt", "w") as f:
        f.write(str(p) + "\n" + str(q) + "\n" + str(Dp) + "\n" + str(Dq))

    with open("Keys/public_key.txt", "w") as f:
        f.write(str(N) + "\n" + str(E))

def chiffrement_RSA(string):
    # Lecture du fichier clé publique
    with open('Keys/public_key.txt') as fichier:
        E, N = fichier.readlines()
    E = int(E)
    N = int(N)

    for carac in string:
        asciicarac = ord(carac)
        carac_pow = pow(asciicarac, E)
        carac_crypt = carac_pow % N
        liste_chif.append(carac_crypt)
    return(liste_chif)

def dechiffrement_RSA(liste_chif):
    """ Dechiffre un message RSA, lit la valeur de clé dans le fichier
        Input  : str - chiffré
        Output : str - clair
    """

    with open('Keys/private_key_PKCS.txt') as fichier:
        p, q, Dp, Dq, q_inv  = fichier.readlines()
    p = int(p)
    q = int(q)
    Dp = int(Dp)
    Dq = int(Dq)
    q_inv = int(q_inv)
    p_inv = identite_bezout(p,q)[1]
    pq = p * q

    for c in liste_chif:
        Mp = pow(c, Dp) % p
        Mq = pow(c, Dq) % q
        mb = (Mp - Mq) * q
        clair1 = (Mp*q*q_inv)+(Mq*p*p_inv)
        clair2 = (mb*q_inv)+Mq
        print(clair1, clair2)
        #print(chr(clair))

    message_clair = ''.join(liste_dechif)
    #print(message_clair)
    pass

def signature_RSA():
    pass

def verif_signature_RSA():
    pass

def main():
    pass

if __name__ == "__main__":
    main()
