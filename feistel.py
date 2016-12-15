from GS15lib import left_padding, decoupage_string
from CONST import SBOX_LIST, INDICE_PERMUTATION_FEISTEL

def developpement_Feistel(listeInput):
    """Input  : str
       Output : str
    """
    listeOutput =  listeInput[-1] + listeInput[0:5]
    for i in range(1,7):
        listeOutput += listeInput[i*4-1:i*4+5]
    listeOutput += listeInput[-5:] + listeInput[0]
    return(listeOutput)

def sbox_Feistel(blocInput, sbox):
    """Input  : str, list[int]
       Output : str
    """
    indiceLigne = int(blocInput[0] + blocInput[-1], 2)
    indiceColonne = int(blocInput[1:-1], 2)
    blockOutput = left_padding(bin(sbox[indiceLigne][indiceColonne])[2:], "0", 4)
    return(blockOutput)

def permutation_Feistel(blocInput):
    """Input  : str, str
       Output : str
    """
    blockOutput = ""
    for indice in INDICE_PERMUTATION_FEISTEL:
        blockOutput += str(blocInput[indice - 1])
    return(blockOutput)

def feistel(D, K):
    """Input  : str, str
       Output : str      --> F[N](D, K) = FO
    """

    # Calcul de la sortie de Feistel (FO=Feistel Output)
    DP = developpement_Feistel(D)                                                       # Développement de D en D'
    B = left_padding(bin(int(DP, 2) ^ int(K, 2))[2:], "0", 48)                          # D' xor K = B
    listeB = decoupage_string(B, 6)                                                     # Découpage de B en 8 blocs de 6 bits
    C = "".join([sbox_Feistel(bloc, SBOX_LIST[i]) for i, bloc in enumerate(listeB)])    # Application des SBox aux blocs Bx
    FO = permutation_Feistel(C)

    return(FO)


def main():
    pass

if __name__ == "__main__":
    main()
