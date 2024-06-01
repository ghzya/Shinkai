import os
import string
from pprint import pprint

env = os.environ.items()
env_vars = []

hostname = os.getenv('username')

for key, value in env:
    env_vars.append(key)

for key in env_vars:
    value = os.getenv(key)
    if hostname in value:
        continue
    # print(f'{key}: {value}')

#  build environtment mapping dictionary
env_mapping = {}
for character in string.printable:
    env_mapping[character] = {}
    for var in env_vars:
        value = os.getenv(var)
        if character in value:
            env_mapping[character][var] = []
            for i, c in enumerate(value):
                if character == c:
                    env_mapping[character][var] = i

pprint(env_mapping)

def envhide_obfuscate(string):
    new_string = []
    for c in string:
        possible_vars = env_mapping[c]
        new_string = f'{possible_vars}'
    pprint(new_string)

        