from GS15lib import *
import random

""" 1. Generation des cles
        TODO Nb premiers : Tableau ou calcul
        OK Clé chiffrement/ déchiffrement
    2. Ecriture des clés vers fichier
        OK Export fichier
        TODO Séparer le dossier
    3. Chiffrement utilisant clé publique
        OK
    4. Déchiffrement avec clé privée
        OK
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
    print("Clé publique de chiffrement ( {}, {} )".format(N, E))

    # Ecriture des clés publiques et privées dans un fichier
    # TODO Ecrire dans dossier de clés
    with open("Keys/public_key.txt", "w") as fichier:
        fichier.write(str(N) + "\n" + str(E))
    return

def private_key(PHI=int):
    # Lecture du fichier de clé publique - Deuxieme ligne
    with open('Keys/public_key.txt') as fichier:
        E = fichier.readlines()[1]

    D = identite_bezout(int(E),PHI)[1]

    with open("Keys/private_key.txt", "w") as fichier:
        fichier.write(str(D))

    # Clé secrete : (p, q, Dp, Dq, q_inv)
    p = 35
    q = 54
    q_inv = identite_bezout(q,p)[1]
    Dp = D % (p-1)
    Dq = D % (q-1)

    with open("Keys/private_key.txt", "w") as fichier:
        fichier.write(str(p) + "\n" + str(q) + "\n" + str(Dp) + "\n" + str(Dq) + "\n" + str(q_inv))
    return

def generation_keys():
    n = 457
    p = 41
    module = n*p
    PHI = (n-1)*(p-1)

    # Appel sous-fonction de clé publique
    public_key(n, PHI)
    # Appel sous-fonction clé privée
    private_key(PHI)



def chiffrement_RSA(string):
    """ Chiffrement de string avec clé publique
        Input  :
        Output :
        """
    # alternative : open('message.txt', 'r') as message
    #message = input('\nEntrez le mot à chiffrer : ')

    for carac in string:
        asciicarac = ord(carac)
        carac_pow = pow(asciicarac, E)
        carac_crypt = carac_pow % NP
        liste_chif.append(carac_crypt)
    print(liste_chif)
    return(liste_chif)

def dechiffrement_RSA(string):
    """ Dechiffre un message RSA, lit la valeur de clé dans le fichier
        Input  : str - chiffré
        Output : str - clair
    """

    # TODO PKCS
    # Au lieu de m = c^d % NP
    # Mp = c^Dp % p
    # Mq = c^Dq % q
    # m congru à Mp mod P et à Mq mod Q
    for chif in liste_chif:
        ascii = pow(chif, D) % NP
        dechif = chr(ascii)
        liste_dechif.append(dechif)

    message_clair = ''.join(liste_dechif)
    return(message-clair)

def signature_RSA():

    pass

def verif_signature_RSA():

    pass

def main():
    generation_keys()

if __name__ == "__main__":
    main()