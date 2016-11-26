#   Chiffrement RSA
#   Detail des etapes

# 1. Generation des cles
#
#       Choix de N et P deux nombres premiers distincts
#       Calculer leur produit NP = Module de chiffrement
#       Calculer l'indicatrice d'Euler PhiN (Ici N-1 x P-1)
#       e : Choisir un entier naturel e premier avec PhiN
#       d : Inverse de e modulo PhiN (inferieur) - Exposant de chiffrement
#
#
# 2. Ecriture des clés publiques et privées dans un fichier
#
# 3. Chiffrement de message avec la clé publique
#       C congru à M^e modulo n
#       C est choisi strictement inférieur à n
#
# 4. Dechiffrement avec la clé privée
#
#
# 5. Generer une signature avec la clé privée
#
# 6. Vérifier une signature en utilisant la clé publique
#
# 7. RSA avec padding PKCS

