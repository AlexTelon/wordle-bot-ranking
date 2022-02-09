import random

with open('words.txt', 'r') as f:
    WORDS = f.read().splitlines()

def next_word(user_name, n, prev_word):
    """For now I want a deterministic randomness"""
    random.seed(f"{user_name}{n}{prev_word}")
    return random.choice(WORDS)