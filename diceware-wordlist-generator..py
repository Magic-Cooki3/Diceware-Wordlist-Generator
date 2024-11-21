#!/usr/bin/env python
import random
import nltk
from nltk.corpus import words

# Ensure the words corpus is downloaded
nltk.download('words')

def generate_diceware_list():
    """Generate a Diceware word list with identifiers from 11111 to 66666."""
    # Get the list of words from the NLTK corpus
    word_list = words.words()
    
    # Filter words to only include those with 5 or more letters
    filtered_words = [word for word in word_list if len(word) >= 5]
    
    # Ensure we have enough words for identifiers from 11111 to 66666 (55,556 total)
    if len(filtered_words) < 55556:
        raise ValueError("Not enough words in the corpus to assign a unique identifier from 11111 to 66666.")

    # Randomly select 55,556 words and zip them with identifiers
    selected_words = random.sample(filtered_words, 55556)
    identifiers = [f"{i:05d}" for i in range(11111, 66667)]
    
    return list(zip(identifiers, selected_words))

def save_to_file(word_list, filename='diceware_list.txt'):
    """Save the word list to a text file in the specified format."""
    with open(filename, 'w') as file:
        for identifier, word in word_list:
            file.write(f"{identifier}\t{word.lower()}\n")  # Convert word to lowercase
    print(f"Your random Diceware list has been saved to {filename}")

if __name__ == "__main__":
    diceware_list = generate_diceware_list()
    save_to_file(diceware_list)
