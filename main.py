import sys
import GS15lib


messageAcceuil = """
Selectionner votre fonction de chiffrement
->1<- Chiffrement symétrique VCES
->2<- Chiffrement RSA avec module multiple
->3<- Signature RSA avec module multiple
->4<- Déciffrement RSA
->5<- Vérifier une signature RSA
"""

def chiffrement_VCES():
    pass

def chiffrement_RSA():
    pass

def signature_RSA():
    pass

def dechiffrement_RSA():
    pass

def verif_signature_RSA():
    pass

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
        chiffrement_RSA()
    elif choix == 3:
        signature_RSA()
    elif choix == 4:
        dechiffrement_RSA()
    elif choix == 5:
        verif_signature_RSA()

if __name__ == "__main__":
    sys.exit(main())