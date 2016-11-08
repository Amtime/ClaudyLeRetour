from CONST import *
from GS15lib import *

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

def decalage_circulaire(blocInput, n):
    """Input  : str, int
    Output : str
    """
    if n in [1, 2, 9, 16]:
        return(blocInput[-1] + blocInput[:-1])
    else:
        return(blocInput[-2:] + blocInput[:-2])

def permutation_PC1_Feistel(blocInput):
    """Input  : str
       Output : str, str
    """
    KG0 = ""; KG1 = ""
    for i in PC1G_FEISTEL:
        KG0 += blocInput[PC1G_FEISTEL]
    for i in PC1D_FEISTEL:
        KD0 += blocInput[PC1G_FEISTEL]
    return(KG0, KD0)

def permutation_PC2_Feistel(KG, KD):
    """Input  : str, str
       Output : str, str
    """
    KGO = ""; KDO = "";
    for i in PC2G_FEISTEL:
        KGO += KG[i]
    for i in PC2D_FEISTEL:
        KDO += KD[i]
    return(KG0 + KD0)

def generation_clefs(K):
    """Génère les 16 clefs
       Input  : str
       Output : list[str]
    """
    clef = [K]
    KG, KD = permutation_PC1_Feistel(K)
    for i in range(1, 16):
        KG, KD = decalage_circulaire(KG), decalage_circulaire(KD)
        clef.append(permutation_PC2_Feistel(KG, KD))

def feistel(D, K):
    """Input  : str, str
       Output : str      --> F[N](D, K) = FO
    """

    # Calcul de la sortie de Feistel (FO=Feistel Output)
    DP = developpement_Feistel(D)                                                       # Développement de D en D'
    B = left_padding(bin(int(DP, 2) ^ int(clef, 2))[2:], "0", 48)                       # D' xor K = B
    listeB = decoupage_string(B, 6)                                                     # Découpage de B en 8 blocs de 6 bits
    C = "".join([sbox_Feistel(bloc, SBOX_LIST[i]) for i, bloc in enumerate(listeB)])    # Application des SBox aux blocs Bx
    FO = permutation_Feistel(C)

    return(FO)


def main():
    pass

if __name__ == "__main__":
    main()
