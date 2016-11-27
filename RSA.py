from GS15lib import *
import random

#   Chiffrement RSA
#   Detail des etapes

# 1. Generation des cles
#
#       Choix de N et P deux nombres premiers distincts
N = 1151
P = 76733

#       Calculer leur produit NP = Module de chiffrement
NP = N*P

#       Calculer l'indicatrice d'Euler PHI (Ici N-1 x P-1)
PHI = (N-1)*(P-1)

#       E : Choisir un entier naturel e premier avec PhiN - Exposant de chiffrement
#           TQ PGCD(E, P-1) = 1 & PGCD(E, Q-1) = 1
#           TQ PGCD(E, PHI) = 1

tuple = (0, 0, 0)
while tuple[0] != 1:
    E = random.randrange(N, P)
    tuple = identite_bezout(E, PHI)

#       D : Inverse de E modulo PHI - Exposant de déchiffrement
#       Calcul d'inverse avec algo Euclide Etendu
inverse = inv_modulo(E,PHI)
print(inverse)

# 2. Ecriture des clés publiques et privées dans un fichier

# 3. Chiffrement de message avec la clé publique
#       C congru à M^e modulo n
#       C est choisi strictement inférieur à n

# 4. Dechiffrement avec la clé privée
#
#
# 5. Generer une signature avec la clé privée
#
# 6. Vérifier une signature en utilisant la clé publique
#
# 7. RSA avec padding PKCS

