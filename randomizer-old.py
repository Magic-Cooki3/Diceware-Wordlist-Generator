import random
import string

def randomize_text(input_text):
    """
    Randomize text by adding numbers, special characters, spaces and changing capitalization.
    
    Args:
        input_text (str): The input text to be randomized
    
    Returns:
        str: The randomized text
    """
    # Convert input to list for easier manipulation
    text_list = list(input_text)
    
    # Function to insert random character at random position
    def insert_random(char_list, items, count):
        for _ in range(count):
            pos = random.randint(0, len(char_list))
            char_list.insert(pos, random.choice(items))
        return char_list

    # Randomly capitalize existing letters (0-10 times)
    caps_count = random.randint(0, 10)
    letter_positions = [i for i, char in enumerate(text_list) if char.isalpha()]
    if letter_positions:
        for _ in range(min(caps_count, len(letter_positions))):
            pos = random.choice(letter_positions)
            text_list[pos] = text_list[pos].upper()
            letter_positions.remove(pos)

    # Add random numbers (0-10)
    numbers = random.randint(0, 10)
    text_list = insert_random(text_list, string.digits, numbers)

    # Add random spaces (0-5)
    spaces = random.randint(0, 5)
    text_list = insert_random(text_list, [' '], spaces)

    # Replace random letters with numbers (0-10 times)
    replacements = {
        'a': '4', 'e': '3', 'i': '1',
        'o': '0', 's': '5', 't': '7'
    }
    replace_count = random.randint(0, 10)
    letter_positions = [i for i, char in enumerate(text_list) 
                       if char.lower() in replacements]
    if letter_positions:
        for _ in range(min(replace_count, len(letter_positions))):
            if not letter_positions:
                break
            pos = random.choice(letter_positions)
            char = text_list[pos].lower()
            if char in replacements:
                text_list[pos] = replacements[char]
            letter_positions.remove(pos)

    # Add random special characters (0-10)
    special_chars = '$@#!&*()%'
    special_count = random.randint(0, 10)
    text_list = insert_random(text_list, special_chars, special_count)

    return ''.join(text_list)

# Example usage
if __name__ == "__main__":
    input_text = input("Enter text to randomize: ")
    result = randomize_text(input_text)
    print("\nRandomized text:")
    print(result)
