import random
from string import printable

from DES import DES_encryption, DES_decryption
from AES import AES_encryption, AES_decryption
from GS15lib import left_padding, decoupage_string

NB_TOURS_VCES = 10
NB_TOURS_DES = 1
NB_TOURS_AES = 1

def VCES_encryption(bloc, key):
    """ Input  : str - 128 bits, str - 128 bits
        Output : str
    """
    keyDES = "".join([left_padding(bin(ord(char))[2:], "0", 8) for char in key[:8]])
    keyAES = [ord(char) for char in key]
    # Conversion de bloc char -> bin
    blocBin = "".join([left_padding(bin(ord(char))[2:], "0", 8) for char in bloc])
    for i in range(NB_TOURS_VCES):
        # DES prends des chaînes de caractères binaires en entrée
        cipherDES = DES_encryption(blocBin[:64], keyDES, NB_TOURS_DES) + DES_encryption(blocBin[64:], keyDES, NB_TOURS_DES)
        blocInt = [int(octet, 2) for octet in decoupage_string(cipherDES, 8)]
        # AES prends des listes d'entiers en entrée
        cipherAES = AES_encryption(blocInt, keyAES, NB_TOURS_AES)
        blocBin = "".join([left_padding(bin(octet)[2:], "0", 8) for octet in cipherAES])
    return(blocBin)

def VCES_decryption(bloc, key):
    """ Input  : str - 128 bits, str - 128 bits
        Output : str
    """
    keyDES = "".join([left_padding(bin(ord(char))[2:], "0", 8) for char in key[:8]])
    keyAES = [ord(char) for char in key]
    # Conversion de bloc char -> bin
    blocInt = [int(octet, 2 ) for octet in decoupage_string(bloc, 8)]


    for i in range(NB_TOURS_VCES):
        # AES prends des listes d'entiers en entrée
        cipherAES = AES_decryption(blocInt, keyAES, NB_TOURS_AES)
        blocBin = decoupage_string("".join([left_padding(bin(octet)[2:], "0", 8) for octet in cipherAES]), 64)
        # DES prends des chaînes de caractères binaires en entrée
        cipherDES = DES_decryption(blocBin[0], keyDES, NB_TOURS_DES) + DES_decryption(blocBin[1], keyDES, NB_TOURS_DES)
        blocInt = [int(octet, 2) for octet in decoupage_string(cipherDES, 8)]

    return("".join(chr(char) for char in blocInt))

def VCES_key_generation(string):
    random.seed(string)
    indiceListe = "".join([str(random.getstate()[1][i])[:8] for i in range(4)])
    key = ""
    for indice in decoupage_string(indiceListe, 2):
        key += printable[int(indice)]
    return(key)


def main():
    pass

if __name__ == "__main__":
    main()
