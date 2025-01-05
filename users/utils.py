import random
import string


def generate_verification_code():
    "Generate a random six-digit verification code."
    return random.randint(100000, 999999)


def generate_password():
    "Generate a random eight characters password."
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(8))
    return password
