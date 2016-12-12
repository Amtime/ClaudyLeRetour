from GS15lib import decoupage_string, left_padding
from CONST import SUBBYTE_BOX, RCON, SHIFT_ROW_BOX, GALOIS_MULTIPLICATION_2, GALOIS_MULTIPLICATION_3


def AES_encryption(bloc, key, rondes):
    """ Input  : [int], int, [int]
        Output : [int]
    """

    print("bloc de base        : {}".format([left_padding(hex(i)[2:], "0", 2) for i in bloc]))
    roundKeys = key_expansion(key); r = 0
    print("roundKey            : {}".format([left_padding(hex(i)[2:], "0", 2) for i in roundKeys[r]]))
    state = roundKey_add(bloc, roundKeys[r])
    print("Premier addroundkey : {}".format([left_padding(hex(i)[2:], "0", 2) for i in state]))
    while r < rondes:
        r += 1
        print(r)
        state = transformation_application(state, SUBBYTE_BOX)
        print("SUBBYTE_BOX         : {}".format([left_padding(hex(i)[2:], "0", 2) for i in state]))
        state = shift_row(state)
        print("shift               : {}".format([left_padding(hex(i)[2:], "0", 2) for i in state]))
        state = mix_columns(state)
        print("mix columns         : {}".format([left_padding(hex(i)[2:], "0", 2) for i in state]))
        print("roundKey            : {}".format([left_padding(hex(i)[2:], "0", 2) for i in roundKeys[r]]))
        state = roundKey_add(state, roundKeys[r])
        print("addroundkey finbouc : {}".format([left_padding(hex(i)[2:], "0", 2) for i in state]))

    state = transformation_application(state, SUBBYTE_BOX)
    state = shift_row(state)
    state = roundKey_add(state, roundKeys[r])
    return(state)

def shift_row(bloc):
    """ Input  : [int] - 16 octets
        Output : [int] - 16 octets
    """
    output = [0] * 16
    for i in range(4):
        for j in range(4):
            i1, i2 = SHIFT_ROW_BOX[i][j]
            output[4 * j + i] = bloc[4 * i2 + i1]
    return(output)

def roundKey_add(bloc, roundKey):
    """ Input  : [int] - 16 octets, [int] - 16 octets
        Output : [int] - 16 octets
    """
    output = []
    if len(bloc) != len(roundKey):
        raise("Problème dans roundKey_add")
    for i in range(len(bloc)):
        output.append(bloc[i]^roundKey[i])
    return(output)

def mix_columns(bloc):
    """ input  : [int] - 16 octets
        output : [int] - 16 octets
    """
    output = []
    # Application du mixage des colonnes sur 4 blocs de 8 octets
    for i in range(4):
        # Boucle servant à créer le décalage entre chaque ligne et donc de
        # réaliser la fonction MixColumns d'AES colonne par colonne
        for shift in range(4):
            # XOR entre les 4 éléments de la colonnes
            output.append(\
            transformation_application(bloc[4 * i + shift], GALOIS_MULTIPLICATION_2)^\
            transformation_application(bloc[4 * i + (shift + 1) % 4], GALOIS_MULTIPLICATION_3)^\
            bloc[4 * i + (shift + 2) % 4]^\
            bloc[4 * i + (shift + 3) % 4])
    return(output)

def transformation_application(objet, TRANSFORMATION):
    """ Permet d'appliquer la transformation passée en paramètre
        Input  : int / [int]
        Output : int
    """
    if type(objet) == int:
        octet = left_padding(hex(objet)[2:], "0", 2)
        i1, i2 = int(octet[0], 16), int(octet[1], 16)
        output = TRANSFORMATION[i1][i2]
    elif type(objet) == list:
        output = []
        for octet in objet:
            octet = left_padding(hex(octet)[2:], "0", 2)
            i1, i2 = int(octet[0], 16), int(octet[1], 16)
            output.append(TRANSFORMATION[i1][i2])
    else:
        raise("Erreur de type")
    return(output)


def schedule_core(word, ind):
    """ Input  : [int] - 4 octets
        Output : [int] - 4 octets
    """
    # Rotate
    keyOutput = word[1:] + word[:1]
    #SBox
    for i in range(4):
        keyOutput[i] = transformation_application(keyOutput[i], SUBBYTE_BOX)
    # rcon sur le premier bit
    keyOutput[0] = keyOutput[0] ^ RCON[ind]
    return(keyOutput)


def key_expansion(key):
    """Input  : [int] - 16 / 24 / 30 octets
       Output : [int] - 176 / 208 / 240 octets
    """
    if len(key) == 128 / 8:
        n = 16; b = 176
    elif len(key) == 192:
        n = 24; b = 208
    elif len(key) == 256 / 8:
        n = 32; b = 240
    else:
        raise("Longueur de clef impossible")

    # Création de la clef étendue avec la clef donnée
    expandedKey = list(key)
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
            tmp = expandedKey[-4:]
            for j in range(4):
                expandedKey.append(expandedKey[len(expandedKey) - n] ^ tmp[j])

        # Ajout de 4 octets si la clef fait 256 bits
        if len(key) == 256 / 8 and len(expandedKey) < 240:
            tmp = expandedKey[-4:]
            for i in range(4):
                tmp[i] = transformation_application(tmp[i], SUBBYTE_BOX)
            for i in range(4):
                expandedKey.append(expandedKey[len(expandedKey) - n] ^ tmp[i])

        # Ajout de 8 octets si la clef fait 192 bits ou de 12 octets si la clef fait 256 bits
        if len(key) == 192 / 8:
            for i in range(2):
                tmp = expandedKey[-4:]
                for j in range(4):
                    expandedKey.append(expandedKey[len(expandedKey) - n] ^ tmp[j])
        elif len(key) == 256 / 8 and len(expandedKey) < 240:
            for i in range(3):
                tmp = expandedKey[-4:]
                for j in range(4):
                    expandedKey.append(expandedKey[len(expandedKey) - n] ^ tmp[j])

    return(regroupement_clefs(expandedKey))

def regroupement_clefs(expandedKey):
    """ Permet de regrouper les octets en clefs de 16 octets
        Input  : [int] - 176 / 208 / 240 octets
        Output : [[int]] - 176 / 208 / 240 octets
    """
    tmp = []; output = []
    for octet in expandedKey:
        tmp.append(octet)
        if len(tmp) == 16:
            output.append(tmp)
            tmp = []
    return(output)

def main():
    hexa = "32 43 f6 a8 88 5a 30 8d 31 31 98 a2 e0 37 07 34"
    key = "2b 7e 15 16 28 ae d2 a6 ab f7 15 88 09 cf 4f 3c"
    hexa = [int(i, 16) for i in hexa.split(" ")]
    key = [int(i, 16) for i in key.split(" ")]
    AES_encryption(hexa, key, 2)

if __name__ == "__main__":
    main()
