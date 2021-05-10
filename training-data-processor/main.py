# Convert json file to spaCy format.
import logging
import argparse
import sys
import os
import json
import pickle
import csv

# Takes in a filename is that is an MTurk output CSV, formats into the correct
# Python list of tuples format for SpaCy training set
def read_json(filename: str):
    data = []
    with open(filename, "r") as file:
        csv_in = csv.reader(file, delimiter=",", quotechar="\"", quoting=csv.QUOTE_ALL)
        next(csv_in) # skip the header row
        for row in csv_in:
            text = row[0]
            text_split = list(filter(lambda x: x != "", text.split(" ")))
            for action in json.loads(row[1]):
                entities = []
                for key in action.keys():
                    for index in action[key]["indices"]:
                        start = index[0]
                        start_word = text_split[start]
                        end = index[len(index) - 1]
                        end_word = text_split[end]

                        before_start = 0
                        for i in range(start):
                            before_start += text_split[i].count(start_word)

                        before_end = 0
                        for i in range(end):
                            before_end += text_split[i].count(end_word)
                        
                        start_index = find_nth(text, start_word, before_start) + 1
                        end_index = find_nth(text, end_word, before_end) + len(end_word) + 1
                        entities.append((start_index, end_index, key))
            data.append((text, { "entities": entities }))
    return data

def find_nth(string: str, substring: str, n: int):
    if n == 0:
        return string.find(substring)
    else:
        return string.find(substring, find_nth(string, substring, n - 1) + 1)

if __name__ == "__main__":
    print(read_json("mturk_labels.csv"))