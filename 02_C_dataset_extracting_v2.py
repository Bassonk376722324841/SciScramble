import pandas as pd
import csv
import openpyxl

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


# Extracting information from file...

# Read the file
excel_file = "science_vocab.XLSX"
data_frame = pd.read_excel(excel_file)

# Convert to csv
csv_file = "science_vocab.csv"
data_frame.to_csv(csv_file, index=False)

# Extracting the terms and definitions
terms = data_frame["Word"].tolist()
definitions = data_frame["Definition"].tolist()

# Create the dictionary
vocab_dict = columns_to_dict(terms, definitions)