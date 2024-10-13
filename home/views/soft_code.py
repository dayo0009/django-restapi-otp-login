import random
import re
import string


def generate_verification_code():
    codes = string.digits
    choice = ''.join(random.choices(codes, k=6))
    return choice


def password_contain(password):
    characters = r'[A-Z]+[a-z]+[0-9]'
    if re.search(characters, password):
        return password
    else:
        return False


