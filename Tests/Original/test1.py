def count_vowels():
    st = "ammaradil"
    vowle = ["a", "e", "i", "o", "u"]
    count = 0

    for s in st:
        if s in vowle:
            count = count + 1

    print("Count", count)


class main:
    if __name__ == "__main__":
        count_vowels()
