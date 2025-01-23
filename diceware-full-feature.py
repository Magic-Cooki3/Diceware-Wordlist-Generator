#!/usr/bin/env python
import random
import string
import nltk
import os
import sys
import argparse
from nltk.corpus import words

def generate_diceware_list():
    """Generate a list of words for password creation."""
    try:
        word_list = words.words()
        filtered_words = [word.lower() for word in word_list if len(word) >= 5]
        
        sample_size = min(55556, len(filtered_words))
        selected_words = random.sample(filtered_words, sample_size)
        identifiers = [f"{i:05d}" for i in range(11111, 11111 + sample_size)]
        
        return list(zip(identifiers, selected_words))
    except Exception as e:
        print(f"Error generating wordlist: {e}")
        return []

def save_wordlist(diceware_list, filename='diceware_list.txt'):
    """Save the generated wordlist to a file."""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            for identifier, word in diceware_list:
                file.write(f"{identifier}\t{word}\n")
        print(f"Wordlist saved to {filename}")
        return True
    except Exception as e:
        print(f"Error saving wordlist: {e}")
        return False

def randomize_text(input_text):
    """
    Add random capitalization, special characters, and spaces to text.
    
    Args:
        input_text: The base text to randomize
        
    Returns:
        str: Randomized text with required symbols and random spaces
    """
    if not input_text:
        return ""
        
    text_list = list(input_text)
    symbols = '$@#!&*()%'
    
    def insert_random(char_list, items, min_count, max_count):
        count = random.randint(min_count, max_count)
        for _ in range(count):
            pos = random.randint(0, len(char_list))
            char_list.insert(pos, random.choice(items))
        return char_list

    # Add required capitalization
    letter_positions = [i for i, char in enumerate(text_list) if char.isalpha()]
    if letter_positions:
        caps_count = random.randint(1, max(2, len(letter_positions) // 3))
        for _ in range(caps_count):
            pos = random.choice(letter_positions)
            text_list[pos] = text_list[pos].upper()
            letter_positions.remove(pos)

    # Add required numbers and symbols
    text_list = insert_random(text_list, string.digits, 2, 4)
    text_list = insert_random(text_list, symbols, 6, 15)  # 6-15 symbols
    
    # Add random spaces (0-15)
    text_list = insert_random(text_list, [' '], 0, 15)
    
    # Clean up multiple consecutive spaces
    result = ''.join(text_list)
    while '  ' in result:  # Replace double spaces with single spaces
        result = result.replace('  ', ' ')
    
    return result.strip()  # Remove leading/trailing spaces


def generate_password(diceware_list):
    """Generate a password from the wordlist."""
    if not diceware_list:
        print("Error: No words available in the wordlist")
        return False, ""
        
    try:
        selected_words = random.sample([word for _, word in diceware_list], 
                                     min(6, len(diceware_list)))
        passphrase = ' '.join(selected_words)
        randomized_passphrase = randomize_text(passphrase)
        
        print("\nOriginal passphrase:")
        print(passphrase)
        print("\nRandomized passphrase:")
        print(randomized_passphrase)
            
        return True, randomized_passphrase
        
    except Exception as e:
        print(f"Error generating password: {e}")
        return False, ""

def setup_nltk():
    """Setup NLTK data in user's home directory."""
    try:
        nltk_data_dir = os.path.expanduser('~/nltk_data')
        if not os.path.exists(nltk_data_dir):
            os.makedirs(nltk_data_dir)
        nltk.data.path.append(nltk_data_dir)
        
        print("Downloading required NLTK data...")
        nltk.download('words', quiet=True, download_dir=nltk_data_dir)
        return True
    except Exception as e:
        print(f"Error setting up NLTK: {e}")
        return False

def main():
    """Main program entry point."""
    parser = argparse.ArgumentParser(description='Password randomizer')
    parser.add_argument('--password', nargs='?', const='generate', 
                       help='Generate a randomized password. Optionally provide a string to randomize.')
    args = parser.parse_args()

    try:
        if args.password and args.password != 'generate':
            # Direct string randomization mode
            original_text = args.password
            randomized_text = randomize_text(original_text)
            
            print("\nOriginal text:")
            print(original_text)
            print("\nRandomized text:")
            print(randomized_text)
            return 0
            
        elif args.password == 'generate':
            # Original wordlist-based functionality
            if not setup_nltk():
                print("Failed to setup NLTK. Please check your internet connection.")
                return 1

            print("Generating wordlist...")
            diceware_list = generate_diceware_list()
            
            if not diceware_list:
                print("Failed to generate wordlist")
                return 1
                
            if not save_wordlist(diceware_list):
                return 1
            
            success, _ = generate_password(diceware_list)
            if not success:
                return 1
            
        return 0
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 1
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
