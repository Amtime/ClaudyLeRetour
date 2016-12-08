from GS15lib import decoupage_string, left_padding
from CONST import SUBBYTE_BOX, RCON



def schedule_core(keySnippet, ind):
    """ Input  : [int]
        Output : [int]
    """
    # Rotate
    keyOutput = keySnippet[-1:] + keySnippet[:-1]
    # Conversion
    keyOutput = [left_padding(hex(byte)[2:], "0", 2) for byte in keyOutput]
    #SBox
    for i in range(4):
        ind1 = int(keyOutput[i][0], 16); ind2 = int(keyOutput[i][1], 16)
        keyOutput[i] = left_padding(hex(SUBBYTE_BOX[ind1][ind2])[2:], "0", 2)
    # rcon sur le premier bit
    keyOutput[0] = hex(int(keyOutput[0], 16) ^ RCON[ind])[2:]
    return([int(byte, 16) for byte in keyOutput])


def key_expansion(key):
    """Input  : str(bin)
       Output :
    """
    if len(key) == 128:
        n = 16; b = 176
    elif len(key) == 192:
        n = 24; b = 208
    elif len(key) == 256:
        n = 32; b = 240
    else:
        raise("Longueur de clef impossible")

    expandedKey = [int(byte, 2) for byte in decoupage_string(key, 8)]
    rconCpt = 1

    while len(expandedKey) < b:
        # Ajout de 4 octets
        tmp = expandedKey[-4:]
        tmp = schedule_core(tmp, rconCpt)
        rconCpt += 1
        for i in range(4):
            expandedKey.append(expandedKey[len(expandedKey) - n] ^ tmp[i])

        # Ajout de 12 octets
        for i in range(3):
            pass



def main():
    key_expansion("00001101010010110000110101001011000011010100101100001101010010110000110101001011000011010100101100001101010010110000110101001011")

if __name__ == "__main__":
    main()
