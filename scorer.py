import re
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
    else:
        return guess


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
    return words


def main(words, characters):

    guess = get_guess()
    result = input("Input the result: ")
    if result == "=====":
        return "Congrats!"

    words = filter_words(guess, result, words)
    best_guess = guess_word(words, characters)
    print(best_guess)
    return words


if __name__ == "__main__":
    words = read_words()
    characters = count_characters(words)

    i = 1
    while i <= 6:
        words = main(words, characters)
