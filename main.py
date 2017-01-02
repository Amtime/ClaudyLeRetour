import sys
import feistel
from GS15lib import decoupage_string, right_padding
from VCES import VCES_encryption, VCES_decryption, VCES_key_generation
# from RSA import *


messageAcceuil = """
Selectionner votre fonction de chiffrement
->1<- Chiffrement symétrique VCES
->2<- Déchiffrement symétrique VCES
->3<- Chiffrement RSA avec module multiple
->4<- Signature RSA avec module multiple
->5<- Déchiffrement RSA
->6<- Vérifier une signature RSA
"""



def acquisition_message(string):
    # Taper la chaine de caracteres a chiffrer
    message = str(input(string))
    # TODO Fournir un ficher texte ? - OSEF
    return(message)

def main():
    choix = ""
    while choix not in [1,2,3,4,5]:
        try:
            choix = int(input(messageAcceuil))
        except ValueError:
            continue

    if choix == 1:
        message = acquisition_message("Message : ")
        key = VCES_key_generation(acquisition_message("Key : "))
        print(key)
        # On s'assure que tous les blocs fassent 128 bits en ajoutant du padding au dernier
        message = right_padding(message, "\x00", 16 * ((len(message) // 16) + 1))
        cipher = ""
        for bloc in decoupage_string(message, 16):
            cipher += VCES_encryption(bloc, key)
        print(cipher)

    elif choix == 2:
        cipher = acquisition_message("Message chiffré (binaire) : ")
        key = VCES_key_generation(acquisition_message("Key : "))
        print(key)
        plaintext = ""
        for bloc in decoupage_string(cipher, 128):
            plaintext += VCES_decryption(bloc, key)
        print(plaintext)


    elif choix == 3:
        gen_keys()
        message = acquisition_message("Message : ")
        listechif = chiffrement_RSA(message)
        print(listechif)
        dechiffrement_RSA(listechif)
    elif choix == 4:
        signature_RSA()
    elif choix == 5:
        dechiffrement_RSA()
    elif choix == 6:
        verif_signature_RSA()

if __name__ == "__main__":
    sys.exit(main())
