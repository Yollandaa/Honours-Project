def calculate_vowel_frequency():
    text = "johndoe123"
    vowels = ["a", "e", "i", "o", "u"]
    vowel_count = 0

    for character in text:

        if character.lower() in vowels:
            vowel_count += 1

    print(f"Vowel Count: {vowel_count}")


if __name__ == "__main__":
    calculate_vowel_frequency()
