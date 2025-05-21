# Imports...

import pandas as pd
import random

# Generates an anagram using two separate
# modes (example):
def scramble(text, mode):
    # create list of random characters from the string
    # based on the set difficulty

    if mode == "normal":

        # Create a completely random list of characters
        # from the given string
        scramble_list = random.sample(text, len(text))

        # Join as a new string
        scrambled_text = "".join(scramble_list)

    elif mode == "easy":

        # Create a random list with the first and last
        # characters of the characters being the same

        inner_len = len(text) - 1

        scramble_list = random.sample(text[1:inner_len], len(text[1:inner_len]))

        # Join as a new string with first
        # and last characters kept the same
        scrambled_text = "".join(scramble_list)

        scrambled_text = text[0] + scrambled_text + text[-1]

    return scrambled_text


# Collects terms and definitions and
# pairs them in a dictionary
def columns_to_dict(terms, definitions):
    '''
    Extracts the content from both columns in
    the csv file and returns them as a dictionary
    '''

    # Check that both columns are of the same degree
    if len(terms) != len(definitions):
        return {}
    else:
        return dict(zip(terms,definitions))


# Generates an anagram dictionary
# based on the number of rounds
def anag_generate(rounds, mode):

    # Read the file
    excel_file = "science_vocab.XLSX"
    data_frame = pd.read_excel(excel_file)

    # Convert to csv
    csv_file = "science_vocab.csv"
    data_frame.to_csv(csv_file, index=False)

    # Extracting the terms and definitions
    terms = data_frame["Word"].tolist()
    definitions = data_frame["Definition"].tolist()

    i = 0

    # Remove the rest of the terms
    # and definitions in the list
    terms = terms[-rounds:]
    definitions = definitions[-rounds:]

    # Generate anagrams iteratively
    while i <= rounds-1:
        terms[i] = scramble(terms[i], mode)
        i += 1

    # Create the dictionary
    vocab_dict = columns_to_dict(terms, definitions)

    return terms,vocab_dict


# Example case
rounds = 203
mode = "easy"

terms, vocab_dict = anag_generate(rounds,mode)

random_anagram = random.choice(terms)

print(f"{random_anagram} : {vocab_dict[random_anagram]}")