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

def init_parametres():
    # TODO Meilleur choix de nombres premiers
    n = 457
    p = 41
    global NP
    NP = N*P
    phi = (N-1)*(P-1)

    # TODO Existence dossier de clés
    return

def gen_public_key():
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
    with open("public_key.txt", "w") as fichier:
        fichier.write(str(N) + "\n" + str(E))
    return

def gen_private_key():
    D = identite_bezout(E,PHI)[1]
    print("\nClé privée : ", D)

    # TODO Ecrire dans dossier de clés
    with open("private_key.txt", "w") as fichier:
        fichier.write(str(D))
    return


def chiffrement_RSA(string):
    """ Decoupe une chaîne de caractère en morceau de n caractères. /!\ Si ça ne tombe pas rond la fonction ignore le reste
        Ex : decoupage_string("abcde", 2) --> ["ab", "cd"] # Le "e" est oublié
        Input  :
        Output :
        """
    # alternative : open('message.txt', 'r') as message
    message = input('\nEntrez le mot à chiffrer : ')

    # Chiffrement de message avec la clé publique
    for carac in message:
        asciicarac = ord(carac)
        carac_pow = pow(asciicarac, E)
        carac_crypt = carac_pow % NP
        liste_chif.append(carac_crypt)
    print(liste_chif)

    pass

def dechiffrement_RSA():
    """ Dechiffre un message RSA, lit la valeur de clé dans le fichier
        Input  : str - chiffré
        Output : str - clair
    """
    for chif in liste_chif:
        ascii = pow(chif, D) % NP
        dechif = chr(ascii)
        liste_dechif.append(dechif)

    print(''.join(liste_dechif))
    pass

def signature_RSA():

    pass

def verif_signature_RSA():

    pass