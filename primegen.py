import math, os.path


def test_file():
    if os.path.exists("primes.txt"):
        with open("primes.txt", "rb") as f: last = int(f.readlines()[-1].decode())
        return last
    else:
        with open("primes.txt", "w") as f: f.write("Liste nombres premiers : \n")
        return 3


def prime_gen(start):
    # TODO Menage dans le fichier

    nb_test = start; nb_trouves = 0
    while True:
        is_prime = True
        for x in range(2, int(math.sqrt(nb_test) + 1)):
            if nb_test % x == 0:
                is_prime = False; break
        if is_prime:
            with open("primes.txt", "a") as f: f.write("\n" + str(nb_test))
            nb_trouves += 1
            #print(nb_test)
        nb_test += 1
        if nb_trouves == 100: break


def go_prime():
    start = test_file()
    prime_gen(start)


if __name__ == "__main__":
    go_prime()