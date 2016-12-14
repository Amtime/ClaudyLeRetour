import sys
import feistel
from GS15lib import decoupage_string
from RSA import *


messageAcceuil = """
Selectionner votre fonction de chiffrement
->1<- Chiffrement symétrique VCES
->2<- Chiffrement RSA avec module multiple
->3<- Signature RSA avec module multiple
->4<- Déchiffrement RSA
->5<- Vérifier une signature RSA
"""

def acquisition_message():
    # Taper la chaine de caracteres a chiffrer
    message = str(input("Message : "))
    # TODO Fournir un ficher texte ?
    return(message)

def main():
    choix = ""
    while choix not in [1,2,3,4,5]:
        try:
            choix = int(input(messageAcceuil))
        except ValueError:
            continue

    if choix == 1:
        chiffrement_vces()
    elif choix == 2:
        gen_keys()
        message = acquisition_message()
        listechif = chiffrement_RSA(message)
        print(listechif)
        #dechiffrement_RSA(listechif)
    elif choix == 3:
        signature_RSA()
    elif choix == 4:
        dechiffrement_RSA()
    elif choix == 5:
        verif_signature_RSA()

if __name__ == "__main__":
    sys.exit(main())
