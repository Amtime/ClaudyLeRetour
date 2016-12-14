from operator import mul, mod
from functools import reduce

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

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def reste_chinois(m, a):
    """
    Utilisation dans la création de clé RSA modulo multiple
    :param m: Liste des modulo de chaque equation
    :param a: Liste des congru connus
    :return: Solution - modulo M
    """
    M = reduce(mul, m) # produit des m
    m_i = [M / item for item in m]
    b = map(mod, m_i, m)
    g, k, l = map(egcd, b, m)
    g, k, l = zip(g, k, l)
    t = map(mod, k, m)
    e = map(mul, m_i, t)

    x_sum = sum(map(mul, a, e))
    x = x_sum % M
    return x

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

def main():
    pass

if __name__ == "__main__":
    main()
