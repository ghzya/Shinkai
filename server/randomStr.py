import string
import random


def generateRandomValue():
    char_length = 10
    string_domain = string.ascii_lowercase + string.digits
    generated_random_char = random.choices(string_domain, k=char_length)
    generated_random_string = ''.join(generated_random_char)                      
    return generated_random_string

def main():
    print(generateRandomValue())


if __name__ == "__main__":
    main()