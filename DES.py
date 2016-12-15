from GS15lib import left_padding,decoupage_string
from feistel import feistel
from CONST import PC1G_FEISTEL, PC1D_FEISTEL, PC2_FEISTEL,\
                    PERMUTATION_INITIAL_DES, PERMUTATION_FINALE_DES

def DES_encryption(bloc, K, iteration):
    clef = generation_clefs(K)
    G, D = decoupage_string(permutation_application(bloc, PERMUTATION_INITIAL_DES), 32)   # Permutation initiale + découpage en 2 blocks de 32 bits

    for i in range(iteration):
        FO = feistel(D, clef[i+1])
        DNP = left_padding(bin(int(G, 2) ^ int(FO, 2))[2:], "0", 32)
        G, D = D, DNP

    return(permutation_application(D+G, PERMUTATION_FINALE_DES))


def DES_decryption(bloc, K, iteration):
    clef = generation_clefs(K)
    D, G = decoupage_string(permutation_application(bloc, PERMUTATION_INITIAL_DES), 32)   # Permutation initiale + découpage en 2 blocks de 32 bits

    for i in range(iteration):
        FO = feistel(G, clef[len(clef) - i - 1])
        GNP = left_padding(bin(int(D, 2) ^ int(FO, 2))[2:], "0", 32)
        G, D = GNP, G

    return(permutation_application(G+D, PERMUTATION_FINALE_DES))


def permutation_application(blocInput, PERMUTATION):
    """Input  : str, [int]
       Output : str
    """
    blockOutput = ""
    for indice in PERMUTATION:
        blockOutput += str(blocInput[indice - 1])
    return(blockOutput)

def decalage_circulaire(blocInput, n):
    """Input  : str, int
    Output : str
    """
    if n in [1, 2, 9, 16]:
        return(blocInput[1:] + blocInput[:1])
    else:
        return(blocInput[2:] + blocInput[:2])

def permutation_PC1(blocInput):
    """Input  : str
       Output : str, str
    """
    KG0 = ""; KD0 = ""
    for i in PC1G_FEISTEL:
        KG0 += blocInput[i-1]
    for i in PC1D_FEISTEL:
        KD0 += blocInput[i-1]
    return(KG0, KD0)

def generation_clefs(K):
    """Génère les 16 clefs
       Input  : str
       Output : list[str]
    """
    clef = [K]
    KG, KD = permutation_PC1(K)
    for i in range(1, 17):
        KG, KD = decalage_circulaire(KG, i), decalage_circulaire(KD, i)
        clef.append(permutation_application(KG + KD, PC2_FEISTEL))
    return(clef)


if __name__ == "__main__":
    key = "00010011 00110100 01010111 01111001 10011011 10111100 11011111 11110001".replace(" ", "")
    plaintext = "0000 0001 0010 0011 0100 0101 0110 0111 1000 1001 1010 1011 1100 1101 1110 1111".replace(" ", "")
    ciphertext = DES_encryption(plaintext, key, 16)
    plain = DES_decryption(ciphertext, key, 16)
    print(plaintext)
    print(plain)
