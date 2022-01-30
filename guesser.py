from collections import Counter, defaultdict


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
            return get_evalulation()
    if len(evalulation) != 5:
        print("Result must be 5 characters long.")
        return get_evalulation()
    if evalulation == "=====":
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


def is_valid_word(word, char, evals):
    truths = []
    for pair in evals:
        for idx, eval in pair.items():
            if eval == "=":
                truths.append(word[idx] == char)
            elif eval == "+":
                truths.append(char in word and word[idx] != char)
            elif eval == "-":
                truths.append(char not in word)
            else:
                raise ValueError(f"Something is wrong with the result.")
    return any(truths)


def filter_word_bank(guess, result, words):
    """
    TODO: Redo this with regex

    guess : word that was guessed (str)
    result : "=" for correct char and place, "+" for correct char wrong place, "-" for incorrect char
    """
    if result is None:
        return None

    chareval = defaultdict(list)
    for idx, (char, eval) in enumerate(zip(guess, result)):
        chareval[char].append({idx: eval})

    for char, evals in chareval.items():
        words = [word for word in words if is_valid_word(word, char, evals)]

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
        words = main(words, characters)
        if words is None:
            print(f"Congratulations! You won in {n_tries}!")
            break
        n_tries += 1
