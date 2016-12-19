from operator import mul, mod
from functools import reduce
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


def decoupage_string(string, n):
    """ Decoupe une chaîne de caractère en morceau de n caractères. /!\ Si ça ne tombe pas rond la fonction ignore le reste
        Ex : decoupage_string("abcde", 2) --> ["ab", "cd"] # Le "e" est oublié
        Input  : str, int
        Output : list[str]
    """
    output = []
    for i in range(len(string) // n):
        output.append(string[i*n: i*n + n])
    return(output)


def left_padding(string, char, length):
    """Sert principalement à compléter les 0 à gauche des nombres en binaires"""
    output = string
    while len(output) < length:
        output = char + output
    return(output)


def random_bytes(length, output = ""):
    while len(output) < length:
        output = str(random.randint(0, 1)) + output
    return output


def main():
    print(random_bytes(32))
    pass

if __name__ == "__main__":
    main()
