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

def public_key(N, PHI):
     while(True):
         E = random.randint(1, PHI)
         if E % 2 != 0 :
             if identite_bezout(E, PHI)[0]==1:
                 break
             else:
                 E = random.randint(1, PHI)
         else:
             E = random.randint(1, PHI)

    with open("Keys/public_key.txt", "w") as f:
        f.write(str(N) + "\n" + str(E))

    print("Clé publique ok, E : ", E)
    print("module chiffrement N : ", N)

def private_key(p, q, PHI):
    # Lecture de la clé publique et calcul de l'inverse
    with open('Keys/public_key.txt') as f:
        E = f.readlines()[1]
    D = identite_bezout(int(E),PHI)[1]

    Dp = D % (p-1)
    Dq = D % (q-1)
    q_inv = identite_bezout(q,p)[1]
    print("Clé privée D : ", D)

    with open("Keys/private_key_PKCS.txt", "w") as f:
        f.write(str(p) + "\n" + str(q) + "\n" + str(D) + "\n" + str(Dp) + "\n" + str(Dq) + "\n" + str(q_inv))

def gen_keys():
    """
    Génère les fichiers de clé :
        - public_key.txt avec N, E
        - private_key_PKCS.txt avec p, q, Dp, Dq
    """
    n1 = 19 # PRIMES[random.randint(0, len(PRIMES))]
    n2 = 43 # PRIMES[random.randint(0, len(PRIMES))]
    N = n1 * n2
    phi = (n1-1)*(n2-1)

    public_key(N, phi)
    private_key(n1, n2, phi)
    # p et q :
    # - Premiers
    # - PGCD(p-1, q-1) = 2

def chiffrement_RSA(string):
    # Lecture du fichier clé publique
    with open('Keys/public_key.txt') as f:
        E, N = f.readlines()
    E = int(E); N = int(N)

    liste_chif = []
    for carac in string:
        asciicarac = ord(carac)
        carac_pow = pow(asciicarac, E) % N
        liste_chif.append(carac_pow)
    return(liste_chif)

def dechiffrement_RSA(liste_chif):
    """ Dechiffre un message RSA, lit la valeur de clé dans le fichier
        Input  : list.int - chiffré
        Output : clair
    """
    with open('Keys/private_key_PKCS.txt') as f:
        p, q, D, Dp, Dq, q_inv  = f.readlines()
    with open('Keys/public_key.txt') as f:
        E, N = f.readlines()
    p = int(p); q = int(q); q_inv = int(q_inv); Dp = int(Dp); Dq = int(Dq); D = int(D); N = int(N)

    liste_dechif = []
    for c in liste_chif:
        m1 = pow(c, Dp) % p
        m2 = pow(c, Dq) % q
        h = (q_inv * (m1 - m2)) % p
        print("H: ",h)
        print("m1-m2: ",m1-m2)
        # Ajout p pour garder la somme positive
        clair = m2 + (h * q)
        liste_dechif.append(chr(clair))

    liste_dechif2 = []
    for c in liste_chif:
        ascii = pow(c, D) % N
        dechif = chr(ascii)
        liste_dechif2.append(dechif)

    message_clair = ''.join(liste_dechif)
    print(message_clair)
    message_clair2 = ''.join(liste_dechif2)
    print(message_clair2)

def signature_RSA():
    pass

def verif_signature_RSA():
    pass

def main():
    pass

if __name__ == "__main__":
    main()