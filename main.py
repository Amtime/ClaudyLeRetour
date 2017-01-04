import sys
import feistel
from GS15lib import decoupage_string, right_padding
from VCES import VCES_encryption, VCES_decryption, VCES_key_generation
from RSA import gen_cles, chiffrement, dechiffrement, gen_signature, check_signature


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
    return(message)


def main():
    choix = ""
    while choix not in [1,2,3,4,5,6]:
        try:
            choix = int(input(messageAcceuil))
        except ValueError:
            continue

    if choix == 1:
        message = acquisition_message("Message : ")
        key = VCES_key_generation(acquisition_message("Key : "))
        # On s'assure que tous les blocs fassent 128 bits en ajoutant du padding 
        message = right_padding(message, "\x00", 16 * ((len(message) // 16) + 1))
        cipher = ""
        for bloc in decoupage_string(message, 16):
            cipher += VCES_encryption(bloc, key)
        print(cipher)

    elif choix == 2:
        cipher = acquisition_message("Message chiffré (binaire) : ")
        key = VCES_key_generation(acquisition_message("Key : "))
        plaintext = ""
        for bloc in decoupage_string(cipher, 128):
            plaintext += VCES_decryption(bloc, key)
        print(plaintext)


    elif choix == 3:
        # Chiffrement RSA avec module multiple

        print("Utiliser les clés présentes dans le dossier Keys ? y/n\nSi non changer les fichiers")
        reponse = str(input())

        if reponse == "y": pass
        elif reponse == "n": gen_cles()
        else: return "Terminé"

        message = acquisition_message("Message : ")

        chiffrement(message, 'Keys/public_key.txt')
        print("\nTerminé, voir fichier : RSA-Cypher-Output.txt")

    elif choix == 4:
        # Signature RSA avec module multiple
        with open('Keys/private_key_PKCS.txt') as f:
            d, n, p, q, q_inv, dp, dq = f.readlines()
        cle_secrete = int(d), int(n), int(p), int(q), int(q_inv), int(dp), int(dq)
        gen_signature("01001101001", cle_secrete)

    elif choix == 5:
        # Dechiffrement RSA
        print("Utilisation de la clé privée du dossier Keys..")
        dechiffrement('Keys/private_key_PKCS.txt')
        print("\nTerminé, voir fichier : RSA-Clear-Output.txt")

    elif choix == 6:
        # Verification signature RSA
        with open('Keys/public_key.txt') as f:
            e, n, x1, x2, x3, x4, x5 = f.readlines()
        cle_publique = int(e), int(n), x1, x2, x3, x4, x5
        f.close()

        check_signature(cle_publique)

if __name__ == "__main__":
    sys.exit(main())
