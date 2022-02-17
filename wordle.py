import random

with open('words.txt', 'r') as f:
    WORDS = f.read().splitlines()

def valid_guess(guess):
    return guess in WORDS

def next_word(user_name, i, prev_word):
    """For now I want a deterministic randomness.

    The combination of user_name, which word they are on and previous word should suffice for now.

    This should ensure that words are deteministic, random and will not get stuck in cycles.
    """
    random.seed(f"{user_name}{i}{prev_word}")
    return random.choice(WORDS)


if __name__ == "__main__":
    print('Evaluation of how we generate the random words!')
    print()
    user_name = f'alex{random.randint(0, 10_000)}'

    from collections import Counter
    from itertools import count as count_from
    from statistics import mean
    import statistics

    counter = Counter()
    never_picked = set(WORDS)

    _90 = False

    word = ""
    for i in count_from(0):
        word = next_word(user_name, i, prev_word=word)
        counter[word] += 1

        if word in never_picked:
            never_picked.remove(word)

        if not _90 and len(never_picked) / len(WORDS) <= 0.1:
            print(f"{i} iterations until 90% of words have been picked")
            print('Stats about how often words have appeared:')
            print(f"Average {mean(counter.values()):.3f}")
            print(f"Median  {statistics.median(counter.values())}")
            print(f"Max     {max(counter.values())}")
            print()
            _90 = True

        if not never_picked:
            print(f"{i} iterations until 100% of words have been picked ({len(WORDS)} words)")
            print('Stats about how often words have appeared:')
            print(f"Average {mean(counter.values()):.3f}")
            print(f"Median  {statistics.median(counter.values())}")
            print(f"Max     {max(counter.values())}")
            print()
            break