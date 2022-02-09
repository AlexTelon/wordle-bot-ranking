import random

with open('words.txt', 'r') as f:
    WORDS = f.read().splitlines()


def gen_words(user_name, n):
    random.seed(f"{user_name}{n}")
    while True:
        yield random.choice(WORDS)