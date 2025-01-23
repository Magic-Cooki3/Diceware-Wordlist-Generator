# Diceware Password Generator

This project generates a Diceware word list with unique identifiers to help create strong, memorable passwords. Each identifier corresponds to a word that is at least 5 letters long, ensuring a robust passphrase.

The idea is that you roll 5 6-sided dice, put them in a random order, correlate that number to the number in the wordlist and then write it down and do this 6+ times then add some numbers, caps, and special characters.

This program aims to give every user a new wordlist every time it is ran from a wordbank of over 250,000 english words. This way no one will ever have the same password as anyone else and it can be deleted and not narrowed down to what wordlist you used.

## Features

- Generates a list of unique identifiers ranging from `11111` to `66666`.
- Each identifier is paired with a randomly selected word from the NLTK English words corpus.
- All words are guaranteed to be at least 5 letters long.
- Saves the output to a text file in a simple and easy-to-read format.
- create a new diceware list, select 6 random words, and then randomize it and output it all with one command!
   - example: ./full-feature.py --password
- randomize any string, like a diceware password you generated using real dice!
   - example: ./full-feature.py --password {insert string here}

## Requirements

- Python 3.6 or higher
- NLTK python library
- argparse python library

## Example head of txt file generated, it goes to 66666

```
11111	hottentot
11112	esterize
11113	deism
11114	mailless
11115	smartish
11116	fiber
11117	petioliventres
11118	scalelike
11119	homograph
11120	orphism
```
## Tips
Execute the script using "python diceware-wordlist-generator.py" rather than "./diceware-wordlist-generator.py" and instead of double-clicking as for some reason (at least on my systems) it made it makes it run much, much faster, but the inital run may take some time depending on your download speed.
