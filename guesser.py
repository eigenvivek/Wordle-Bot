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
    for character in unique_characters(word):
        score += characters[character]
    return score


def score_word_bank(words, characters):
    word_scores = {word: score_word(word, characters) for word in words}
    word_scores = {
        word: score
        for word, score in sorted(word_scores.items(), key=lambda x: x[1], reverse=True)
    }
    return word_scores


def filter_word_bank(guess, result, words):
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
            return filter_word_bank(guess, result, words)
    return words


def main(words, characters):

    # Get the scores for the top 5 words
    word_scores = score_word_bank(words, characters)
    print({word: score for word, score in list(word_scores.items())[:5]})

    # Input a guess and get the result
    guess = get_guess()
    result = get_evalulation()

    # Filter words based on the result
    words = filter_word_bank(guess, result, list(word_scores.keys()))
    return words


if __name__ == "__main__":

    # Get the words and character counts
    words = read_words()
    characters = count_characters(words)

    n_tries = 1
    while n_tries <= 6:
        try:
            words = main(words, characters)
            n_tries += 1
            break
