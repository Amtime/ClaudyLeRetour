DEBUG = False

def identite_bezout(a, b, i=0, A=0, B=0, x0=1, y0=0, x1=0, y1=1):
    """Entrer l'entier et son modulo
       Output : PGCD(a, b), x, y
    """

    q = a // b; r = a % b
    x = q*x1 + x0; y = q*y1 + y0

    if r == 0:
        return(b, x1, -y1)
    else:
        if DEBUG:
            print("{} = {}*{} + {} <==> {} = {}*{} - {}*{}".format(a, b, q, r, r, A, x, B, y))
            print("x{} = q1*x1 + x0 <==> {} = {}*{} + {}".format(i+2, x, q, x1, x0))
            print("y{} = q1*y1 + y0 <==> {} = {}*{} + {}\n".format(i+2, y, q, y1, y0))
        return(identite_bezout+(b, r, i = i+1, A=A, B=B, x1=x, y1=y, x0=x1, y0=y1))


def main():
    if DEBUG:
        am1 = identite_bezout(13, 7)

if __name__ == "__main__":
    main()
