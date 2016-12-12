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

def public_key(N=int, PHI=int):
    while(True):
        global E
        E = random.randint(1, PHI)
        if(E&1):
            if identite_bezout(E, PHI)[0]==1:
                break
            else:
                E = random.randint(1, PHI)
        else:
            E = random.randint(1, PHI)

    with open("Keys/public_key.txt", "w") as fichier:
        fichier.write(str(N) + "\n" + str(E))
    return

def private_key(PHI=int):
    # Lecture de la clé publique
    with open('Keys/public_key.txt') as fichier:
        E = fichier.readlines()[1]

    D = identite_bezout(int(E),PHI)[1]

    # Ecriture de la clé privée
    with open("Keys/private_key.txt", "w") as fichier:
        fichier.write(str(D))

    # PKCS (p, q, Dp, Dq, q_inv)
    p = random.randint(2, 50)
    q = random.randint(2, 50)
    q_inv = identite_bezout(q,p)[1]
    Dp = D % (p-1)
    Dq = D % (q-1)

    with open("Keys/private_key_PKCS.txt", "w") as fichier:
        fichier.write(str(p) + "\n" + str(q) + "\n" + str(Dp) + "\n" + str(Dq) + "\n" + str(q_inv))
    return

def generation_keys():
    n = PRIMES[random.randint(0, len(PRIMES))]
    p = PRIMES[random.randint(0, len(PRIMES))]
    global NP
    NP = n * p
    PHI = (n-1)*(p-1)

    public_key(n, PHI)
    private_key(PHI)

def chiffrement_RSA(string):
    # Lecture du fichier clé publique
    with open('Keys/public_key.txt') as fichier:
        E = int(fichier.readlines()[1])

    for carac in string:
        asciicarac = ord(carac)
        carac_pow = pow(asciicarac, E)
        carac_crypt = carac_pow % NP
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
