#!/usr/bin/env python
import random
import nltk
from nltk.corpus import words

# Ensure the words corpus is downloaded
nltk.download('words')

def generate_diceware_list():
    """Generate a Diceware word list with identifiers from 11111 to 66666."""
    print("Loading the NLTK words corpus...")
    word_list = words.words()
    
    print("Filtering words to include only those with 5 or more letters...")
    filtered_words = [word for word in word_list if len(word) >= 5]
    
    print(f"Total words found with 5 or more letters: {len(filtered_words)}")
    
    print("Selecting 55,556 random words...")
    selected_words = random.sample(filtered_words, 55556)
    
    print("Generating identifiers...")
    identifiers = [f"{i:05d}" for i in range(11111, 66667)]
    
    print("Zipping identifiers with selected words...")
    return list(zip(identifiers, selected_words))

def save_to_file(word_list, filename='diceware_list.txt'):
    """Save the word list to a text file in the specified format."""
    print(f"Saving the word list to {filename}...")
    with open(filename, 'w') as file:
        for identifier, word in word_list:
            file.write(f"{identifier}\t{word.lower()}\n")  # Convert word to lowercase
    print("Word list saved successfully.")

if __name__ == "__main__":
    try:
        print("Starting Diceware password generator...")
        diceware_list = generate_diceware_list()
        save_to_file(diceware_list)
        print("Diceware password generation complete.")
    except Exception as e:
        print(f"An error occurred: {e}")
