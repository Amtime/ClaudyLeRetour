import random


def identite_bezout(a, b, i=0, x0=1, y0=0, x1=0, y1=1):
    """Input  : int, int
       Output : int, int, int  --> PGCD(a, b), x, y
    """
    q = a // b; r = a % b
    x = q*x1 + x0; y = q*y1 + y0

    if r == 0:
        return(b, x1, -y1)
    else:
        return(identite_bezout(b, r, i=i+1, x1=x, y1=y, x0=x1, y0=y1))


def XOR(x, y, res=""):
    x = str(x); y = str(y)

    if len(x) > len(y):     y = right_padding(y, "0", len(x)) # Completion des chaines
    elif len(x) < len(y):   x = right_padding(x, "0", len(y))

    for i in range(0,len(y)): # Iteration sur 2 strings
        c = x[i] != y[i]
        if c: res += "1"
        else: res += "0"
    return res


def decoupage_string(string, n):
    """ Decoupe une chaîne de caractère en morceau de n caractères. /!\ Si ça ne tombe pas rond la fonction ignore le reste
        Ex : decoupage_string("abcde", 2) --> ["ab", "cd"] # Le "e" est oublié
        Input  : str, int
        Output : list[str]
    """
    output = []
    for i in range(len(string) // n):
        output.append(string[i*n: i*n + n])
    return output


def left_padding(string, char, length):
    """Sert principalement à compléter les 0 à gauche des nombres en binaires"""
    output = string
    while len(output) < length:
        output = char + output
    return output


def right_padding(string, char, length):
    """Sert principalement à compléter les 0 à droite des nombres en binaires"""
    output = string
    while len(output) < length:
        output = output + char
    return output


def right_padding(string, char, length):
    return(string + (length - len(string)) * char)


def random_bytes(length, output = ""):
    while len(output) < length:
        output = str(random.randint(0, 1)) + output
    return output



def main():
    pass


if __name__ == "__main__":
    main()
