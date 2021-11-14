import random
from words import words
import string


def get_valid_word(words):
    word = random.choice(words)
    while '-' in word or ' ' in word:
        word = random.choice(words)

    return word.upper()


def hangman():
    word = get_valid_word(words)
    word_of_letters = set(word)  # letters in words
    alphabet = set(string.ascii_uppercase)  # all alphabets stored as sets
    used_letters = set()  # what we will use to keep track of guessed letters

    lives = 6

    # getting a user input
    while len(word_of_letters) > 0 and lives > 0:
        # letters used
        print('You have ', lives,
              ' left and you have already guessed these letters ', ' '.join(used_letters))

        # what the current word is (ie W - R D)
        word_list = [
            letter if letter in used_letters else '-' for letter in word]
        print('Current word: ', ' '.join(word_list))

        user_letter = input("Guess a letter: ").upper()
        if user_letter in alphabet - used_letters:
            used_letters.add(user_letter)
            if user_letter in word_of_letters:
                word_of_letters.remove(user_letter)
            else:
                lives = lives - 1  # takes away one life if wrong

        elif user_letter in used_letters:
            print("You have already guessed that letter")
        else:
            print("Invalid character. Please try again")

    if lives == 0:
        print("Sorry you died. The word was", word)
    else:
        print('You guessed the word', word, '!!')


hangman()
