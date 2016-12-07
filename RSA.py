from GS15lib import *
import random

#   Chiffrement RSA

""" 1. Generation des cles
        TODO Nb premiers : Tableau ou calcul
        OK Clé chiffrement/ déchiffrement
    2. Ecriture des clés vers fichier
        TODO Export fichier
    3. Chiffrement utilisant clé publique
        OK
    4. Déchiffrement avec clé privée
        OK
    5. Générer une signature avec clé privée
    6. Vérifier signature avec clé publique
    7. RSA avec padding PKCS
"""

N = 457
P = 41
NP = N*P
PHI = (N-1)*(P-1)
COND=0
liste_chif = []
liste_dechif = []


# Virer les cond, changer pour un while-true-break
while(True):
    E = random.randint(1, PHI)
    if(E&1):
        if identite_bezout(E, PHI)[0]==1:
            break
        else:
            E = random.randint(1, PHI)
    else:
        E = random.randint(1, PHI)

print("\nClé publique de chiffrement (", N,",",E,")")
# changer pour .format()

#       D : Dechiffrement
D = identite_bezout(E,PHI)[1]
# vérifier condition X/Y
print("\nClé privée : ", D)

# 2. Ecriture des clés publiques et privées dans un fichier
# Définir fonctions pour centraliser R/W fichiers ?
with open("public_key.txt", "w") as fichier:
    fichier.write(str(N) + "\n" + str(E))

with open("private_key.txt", "w") as fichier:
    fichier.write(str(D))

# alternative : open('message.txt', 'r') as message
message = input('\nEntrez le mot à chiffrer : ')

# 3. Chiffrement de message avec la clé publique
for carac in message:
    print("Chiffrement de : ", carac)
    asciicarac = ord(carac)
    print("Conversion ASCII : ", asciicarac)
    carac_pow = pow(asciicarac, E)
    carac_crypt = carac_pow % NP
    print("Caractère chiffré : ",carac_crypt, "\n")
    liste_chif.append(carac_crypt)
print(liste_chif)

# 4. Dechiffrement avec la clé privée

for chif in liste_chif:
    ascii = pow(chif, D) % NP
    dechif = chr(ascii)
    liste_dechif.append(dechif)

print(''.join(liste_dechif))

# 5. Generer une signature avec la clé privée
#
# 6. Vérifier une signature en utilisant la clé publique
#
# 7. RSA avec padding PKCS