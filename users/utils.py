import random


def generate_verification_code():
    """Generate a random six-digit verification code."""
    return random.randint(100000, 999999)
