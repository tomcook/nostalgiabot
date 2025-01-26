import os
import json
import github
import random
import requests
from pprint import pprint

# Get the GitHub Gist that contains our state database
gh = github.Github(os.environ.get('GIST_TOKEN'))
gist = gh.get_gist(os.environ.get('STATE_DB_GIST'))

stateDb = json.loads(gist.files['state-bluesky.json'].content)

print(f" : Loaded state DB with {len(stateDb)} entries")

# Get the memories DB

req = requests.get(os.environ.get('MEMORY_DB_URL'))
memories = req.json()

print(f" : Loaded memories DB with {len(memories)} memories")

# Randomly select memories from the database, comparing them to the state database
#   to make sure they haven't already been posted. If they have then pick a new one.

print(" : Choosing a random memory")

while True:
    # Find our random memory to post from the DB

    chosenMemory = random.choice(memories)

    print(f" : Checking memory '{chosenMemory['title']}'")

    if chosenMemory['title'] in stateDb:
        print(f" : WARNING: Memory {chosenMemory['title']} already posted; choosing new one...")
        continue
    else:
        break

print(" : Memory Chosen")
print("==================================================================")
pprint(chosenMemory)
print("==================================================================")