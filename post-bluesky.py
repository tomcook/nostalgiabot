import os
import json
import github
import shutil
import regex
import random
import pprint
import requests
from atproto import Client
from atproto import client_utils
from pprint import pprint
from datetime import datetime
from PIL import Image

api = Client()
api.login(os.environ.get('BLUESKY_USERNAME'), os.environ.get('BLUESKY_PASSWORD'))

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

# Download the memory image

response = requests.get(chosenMemory['source'], stream=True)

with open('img.jpg', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)

# Resize image
img = Image.open('img.jpg')
img.save('img_resized.jpg', format="JPEG", quality=50)

# Assemble the skeet text

skeet = client_utils.TextBuilder()
skeet.text(f"{chosenMemory['caption']} Source: ")
skeet.link('Flickr', chosenMemory['flickr_url'])

alt_text = f"{chosenMemory['caption']}"

# TODO: Detect skeets that are too long and loop back to try a new one
#
#skeet_graphemes = regex.findall(r'\X', skeet)
#if len(skeet_graphemes) >= 300:
#    pprint("caption too long, cannot skeet")
#    exit


#print(" : Preview of skeet to be posted")
#print("==================================================================")
#print(skeet)
#print("==================================================================")

# Post to Bluesky!

if "DRY_RUN" in os.environ:
    print(" : Dry Run, exiting without posting to Bluesky")
else:
    with open('img_resized.jpg', 'rb') as f:
        img_data = f.read()

    api.send_image(text=skeet, image=img_data, image_alt=alt_text)

