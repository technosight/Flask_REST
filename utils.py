import string
from random import choice
from pathlib import Path

# get list of names and surnames
data_dir = Path(__file__).resolve().parent / 'data'

names = []
with open(str(data_dir / 'names.txt'), 'r') as fn:
    for line in fn:
        names.append(line.rstrip())

surnames = []
with open(str(data_dir / 'surnames.txt'), 'r') as fs:
    for line in fs:
        surnames.append(line.rstrip())

def get_random_name():
    return choice(names)

def get_random_surname():
    return choice(surnames)

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(choice(letters) for i in range(length))