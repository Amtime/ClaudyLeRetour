from GS15lib import *
from feistel import feistel
from CONST import *

def DES(bloc, K):
    clef = generation_clefs(K)
    G, D = decoupage_string(IP(bloc))   # Permutation initiale + découpage en 2 blocks de 32 bits
    for i in range(16):
        FO = feistel(D, clef[i])
        DNP = left_padding(bin(int(G, 2) ^ int(FO, 2))[2:], "0", 32)
        G, D = D, DNP
    return(FP("".join(G, D)))

def IP(bloc):
    """Input  : str
       Output : str
    """
    blockOutput = ""
    for indice in PERMUTATION_INITIAL_DES:
        blockOutput += str(blocInput[indice - 1])
    return(blockOutput)


def FP(bloc):
    """Input  : str
       Output : str
    """
    blockOutput = ""
    for indice in PERMUTATION_FINALE_DES:
        blockOutput += str(blocInput[indice - 1])
    return(blockOutput)
