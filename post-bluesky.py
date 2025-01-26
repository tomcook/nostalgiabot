import os
import json
import github
import regex
import pprint
import requests
from atproto import Client
from atproto import client_utils
from pprint import pprint
from datetime import datetime

api = Client()
api.login(os.environ.get('BLUESKY_USERNAME'), os.environ.get('BLUESKY_PASSWORD'))

# Get the GitHub Gist that contains our state database
gh = github.Github(os.environ.get('GIST_TOKEN'))
gist = gh.get_gist(os.environ.get('STATE_DB_GIST'))

stateDb = json.loads(gist.files['state-bluesky.json'].content)

print(f" : Loaded state DB with {len(stateDb)} entries")

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

    # Append to the state database

    stateDb[chosenMemory['title']] = {"posted_on":datetime.now().isoformat()}

    gist.edit(files={"state-bluesky.json": github.InputFileContent(content=json.dumps(stateDb, indent=2))})
    print(" : State DB updated")

