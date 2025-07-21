import random

def scramble(text):
    # create list of random characters from the string
    scramble_list = random.sample(text, len(text))

    # Join as a new string
    scrambled_text = "".join(scramble_list)
    return scrambled_text


# Example Usage (using a variety of words
term1 = "Photosynthesis"
term2 = "Fission"
term3 = "Mitosis"
term4 = "Erosion"

term_list = [term1,term2,term3,term4]

for term in term_list:
    print(f"{term} --> {scramble(term)}\n")