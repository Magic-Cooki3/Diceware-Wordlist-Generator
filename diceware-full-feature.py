#!/usr/bin/env python
import secrets
import string
import nltk
import os
import sys
import argparse
from nltk.corpus import words

# Create a secure random generator using secrets.SystemRandom
secure_random = secrets.SystemRandom()

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

def generate_diceware_list():
    """Generate a list of words with fallback options."""
    try:
        # Try using NLTK words
        word_list = words.words()
    except LookupError:
        # Fallback to basic wordlist
        print("Warning: Using fallback wordlist due to NLTK data access failure")
        word_list = [
            "python", "program", "computer", "network", "security",
            "database", "system", "algorithm", "software", "development",
            # Add more words as needed
        ]
    except Exception as e:
        print(f"Error accessing word list: {e}")
        return []
    
    try:
        filtered_words = [word.lower() for word in word_list if len(word) >= 5]
        if not filtered_words:
            raise ValueError("No valid words found after filtering")
            
        sample_size = min(55556, len(filtered_words))
        selected_words = secure_random.sample(filtered_words, sample_size)
        identifiers = [f"{i:05d}" for i in range(11111, 11111 + sample_size)]
        
        return list(zip(identifiers, selected_words))
    except Exception as e:
        print(f"Error processing word list: {e}")
        return []

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
        count = secure_random.randint(min_count, max_count)
        for _ in range(count):
            pos = secure_random.randint(0, len(char_list))
            char_list.insert(pos, secure_random.choice(items))
        return char_list

    # Add required capitalization
    letter_positions = [i for i, char in enumerate(text_list) if char.isalpha()]
    if letter_positions:
        caps_count = secure_random.randint(1, max(2, len(letter_positions) // 3))
        for _ in range(caps_count):
            pos = secure_random.choice(letter_positions)
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
        selected_words = secure_random.sample([word for _, word in diceware_list], 
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
    """Setup NLTK data with proper error handling and installation verification."""
    try:
        # First check if NLTK data already exists
        nltk_data_dir = os.path.expanduser('~/nltk_data')
        words_path = os.path.join(nltk_data_dir, 'corpora', 'words')
        
        if os.path.exists(words_path):
            print("NLTK data already exists, skipping download...")
            return True
            
        print("Setting up NLTK data directory...")
        if not os.path.exists(nltk_data_dir):
            os.makedirs(nltk_data_dir)
        nltk.data.path.append(nltk_data_dir)
        
        # Download with progress indicator
        print("Downloading NLTK words dataset...")
        try:
            nltk.download('words', quiet=False, download_dir=nltk_data_dir, raise_on_error=True)
        except Exception as download_error:
            print(f"\nDownload failed: {download_error}")
            print("\nTrying alternative download method...")
            
            # Alternative download using direct Python download
            import ssl
            try:
                _create_unverified_https_context = ssl._create_unverified_context
            except AttributeError:
                pass
            else:
                ssl._create_default_https_context = _create_unverified_https_context
            
            nltk.download('words', download_dir=nltk_data_dir)
        
        # Verify download
        if os.path.exists(words_path):
            print("NLTK data downloaded successfully!")
            return True
        else:
            raise Exception("Download verification failed")
            
    except Exception as e:
        print(f"\nError during NLTK setup: {e}")
        print("\nTroubleshooting steps:")
        print("1. Check your internet connection")
        print("2. Ensure you have write permissions in your home directory")
        print("3. Try running with administrator privileges")
        print("4. Consider manual installation of NLTK data")
        return False

def main(argv=None):
    """
    Main program entry point that generates a diceware wordlist by default.
    
    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    if argv is None:
        argv = sys.argv[1:]
        
    parser = argparse.ArgumentParser(description='Password randomizer')
    parser.add_argument('--password', nargs='?', const='generate', 
                       help='Generate a randomized password. Optionally provide a string to randomize.')
    args = parser.parse_args(argv)

    try:
        # Default behavior when no arguments provided - just generate wordlist
        if not argv:
            # Step 1: NLTK Setup
            if not os.path.exists(os.path.expanduser('~/nltk_data/corpora/words')):
                if not setup_nltk():
                    print("Failed to setup NLTK. Using fallback functionality.")
            
            # Step 2: Wordlist Generation
            diceware_list = generate_diceware_list()
            
            if not diceware_list:
                print("Failed to generate wordlist")
                return 1
                
            # Step 3: Save Wordlist
            filename = 'diceware_list.txt'
            if save_wordlist(diceware_list, filename):
                print(f"Diceware wordlist generated as {os.path.abspath(filename)}")
                print(50*"-")
                print(f"    - to generate a wordlist, get a passphrase, then have it randomized run the program with the '--password' flag\n    - to enter your own passphrase to have it randomized add a string after the flag ex: '--password [enter string here]")
                return 0
            return 1
            
        # Handle explicit password argument
        if args.password and args.password != 'generate':
            original_text = args.password
            randomized_text = randomize_text(original_text)
            
            print("\nOriginal text:")
            print(original_text)
            print("\nRandomized text:")
            print(randomized_text)
            return 0
            
        # Handle generate flag
        elif args.password == 'generate':
            if not setup_nltk():
                print("Failed to setup NLTK. Using fallback functionality.")
            
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

if __name__ == '__main__':
    sys.exit(main() or 0)
