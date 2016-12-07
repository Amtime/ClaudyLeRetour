from GS15lib import *
import random

#   Chiffrement RSA

""" 1. Generation des cles
        TODO Génération nombres premiers
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

N = 17
P = 41
NP = N*P
PHI = (N-1)*(P-1)
COND=0
liste_chif = []
liste_dechif = []

E = random.randint(1,PHI)
while(COND!=1):
    if(E&1):
        print("OK E impair")
        PGCDEPHI = identite_bezout(E, PHI)
        COND = 1
        if PGCDEPHI[0]==1:
            print("Le compte est bon E: ",E)
            COND = 1
        else:
            COND = 0
            E = random.randint(1, PHI)
    else:
        print("XXXXXXXXX")
        COND = 0
        E = random.randint(1, PHI)

print("\nClé publique de chiffrement (", N,",",E,")")

#       D : Dechiffrement
D = identite_bezout(E,PHI)[1]
print("\nClé privée : ", D)

# 2. Ecriture des clés publiques et privées dans un fichier

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