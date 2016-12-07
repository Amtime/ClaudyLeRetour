from GS15lib import *
import random

#   Chiffrement RSA

""" 1. Generation des cles
        .Initialisation des paramètres
        .Calcul chiffrement E
        .Calcul dechiffrement D
"""

N = 17
P = 41
NP = N*P
PHI = (N-1)*(P-1)
COND=0

E = random.randint(1,PHI)
while(COND!=1):
    if(E&1):
        print("OK E impair")
        PGCDEPHI = identite_bezout(E, PHI)
        COND = 1
        if PGCDEPHI[0]==1:
            print("Le compte est bon")
            COND = 1
        else:
            COND = 0
            E = random.randint(1, PHI)
    else:
        print("XXXXXXXXX")
        COND = 0
        E = random.randint(1, PHI)

print("\nCle publique (", N,",",E,")")

#       D : Inverse de E modulo PHI - Exposant de déchiffrement


# 2. Ecriture des clés publiques et privées dans un fichier

# 3. Chiffrement de message avec la clé publique
#       C congru à M^e modulo n
#       C est choisi strictement inférieur à n

#mot = input('\nEntrez le mot à chiffrer : ')
#taille_du_mot = len(mot)
#i = 0
#while i < taille_du_mot:
#    ascii = ord(mot[i])
#    lettre_crypt = pow(ascii, E) % PHI
#    print("\n Block : ", lettre_crypt,)
#    ascii = pow(lettre_crypt, D) % PHI
#    print("\n Decyph : ", chr(ascii),)
#    i += 1

# 4. Dechiffrement avec la clé privée


# 5. Generer une signature avec la clé privée
#
# 6. Vérifier une signature en utilisant la clé publique
#
# 7. RSA avec padding PKCS