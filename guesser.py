import random
from collections import Counter


def read_words():
    with open("words.txt", "r") as f:
        words = f.read().splitlines()
    return words


def count_characters(words):
    characters = Counter()
    for word in words:
        for character in word:
            characters[character] += 1
    return characters


def get_guess():
    guess = input("Guess a 5-letter word: ")
    if len(guess) != 5:
        print("Word must be 5 letters long.")
        return get_guess()
    if not guess.isalpha():
        print("Invalid word.")
        return get_guess()
    else:
        return guess


def get_evalulation():
    evalulation = input("Input the result: ")
    for char in evalulation:
        if char not in "=+-":
            print("Invalid result, use '=', '+', or '-'.")
            return get_guess()
    if len(evalulation) != 5:
        print("Result must be 5 characters long.")
        return get_guess()
    if evalulation == "=====":
        print("Congrats!")
        return None
    return evalulation


def unique_characters(word):
    """Get the unique characters in a word (i.e., no duplicate letters)."""
    characters = set()
    for character in word:
        characters.add(character)
    return characters


def score_word(word, characters):
    """Score a word based on the value of each of its characters."""
    score = 0
    for character in word:
        score += characters[character]
    return score


def guess_word(words, characters):
    """Find the word with the highest score."""
    best_score = 0
    best_word = ""
    for word in words:
        score = score_word(unique_characters(word), characters)
        if score > best_score:
            best_score = score
            best_word = word
    return best_word


def filter_words(guess, result, words):
    """
    guess : word that was guessed (str)
    result : "=" for correct char and place, "+" for correct char wrong place, "-" for incorrect char
    """
    # TODO: Redo this with regex
    for idx, (char, eval) in enumerate(zip(guess, result)):
        if eval == "=":
            words = [word for word in words if word[idx] == char]
        elif eval == "+":
            words = [word for word in words if char in word and word[idx] != char]
        elif eval == "-":
            words = [word for word in words if char not in word]
        else:
            result = input("Invalid result, try again: ")
            return filter_words(guess, result, words)
    return words


def main(guess, words, characters):

    # Input a guess and get the result
    guess = get_guess()
    result = get_evalulation()

    words = filter_words(guess, result, words)
    best_guess = guess_word(words, characters)
    return best_guess, words


if __name__ == "__main__":
    words = read_words()
    characters = count_characters(words)

    # Pick one of the top-100 words as a starting guess
    word_scores = {}
    for word in words:
        word_scores[word] = score_word(unique_characters(word), characters)
    word_scores = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)
    word_scores = [word for word, _ in word_scores[:100]]
    guess = random.sample(word_scores, k=1)[0]

    i = 1
    while i <= 6:
        try:
            guess, words = main(guess, words, characters)
        except TypeError:
            break
