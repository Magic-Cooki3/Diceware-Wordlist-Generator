# Diceware Password Generator

This project generates a Diceware word list with unique identifiers to help create strong, memorable passwords. Each identifier corresponds to a word that is at least 5 letters long, ensuring a robust passphrase.

The idea is that you roll 5 6-sided dice, put them in a random order, correlate that number to the number in the wordlist and then write it down and do this 6+ times then add some numbers, caps, and special characters.

This program aims to give every user a new wordlist every time it is ran from a wordbank of over 250,000 english words. This way no one will ever have the same password as anyone else and it can be deleted and not narrowed down to what wordlist you used.

## Features

- Generates a list of unique identifiers ranging from `11111` to `66666`.
- Each identifier is paired with a randomly selected word from the NLTK English words corpus.
- All words are guaranteed to be at least 5 letters long.
- Saves the output to a text file in a simple and easy-to-read format.

## Requirements

- Python 3.6 or higher
- NLTK library
