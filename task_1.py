def fact(z):
    if z == 0:
        return 1
    return z * fact(z - 1)


if __name__ == "__main__":
    print(fact(5))
