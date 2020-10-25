import os
import json
import github
import shutil
import random
import requests
from datetime import datetime
from TwitterAPI import TwitterAPI

api = TwitterAPI(os.environ.get('TWITTER_CONSUMER_KEY'), 
                 os.environ.get('TWITTER_CONSUMER_SECRET'),
                 os.environ.get('TWITTER_ACCESS_TOKEN_KEY'),
                 os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'))

# Get the GitHub Gist that contains our state database
gh = github.Github(os.environ.get('GIST_TOKEN'))
gist = gh.get_gist(os.environ.get('STATE_DB_GIST'))

stateDb = json.loads(gist.files['state.json'].content)

print(f" : Loaded state DB with {len(stateDb)} entries")

# Get the memories DB

req = requests.get(os.environ.get('MEMORY_DB_URL'))
memories = req.json()

print(f" : Loaded memories DB with {len(memories)} memories")

# Find our random memory to post from the DB

chosenMemory = random.choice(memories)

print(" : Memory Chosen")
pprint(chosenMemory)

# Download the memory image

response = requests.get(chosenMemory['photo_url'], stream=True)

with open('img.jpg', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)

# Assemble the tweet text

tweet = f"{chosenMemory['caption']} {chosenMemory['flickr_url']}\n\nPhoto By {chosenMemory['photographer']}"

print(tweet)

# Post to Twitter!

# STEP 1 - upload image
file = open('img.jpg', 'rb')
data = file.read()
r = api.request('media/upload', None, {'media': data})
print('UPLOAD MEDIA SUCCESS' if r.status_code == 200 else 'UPLOAD MEDIA FAILURE: ' + r.text)

# STEP 2 - post tweet with a reference to uploaded image
if r.status_code == 200:
    media_id = r.json()['media_id']
    r = api.request('statuses/update', {'status': tweet, 'media_ids': media_id})
    if r.status_code == 200: 

        twitterPostData = json.loads(r.text)

        print('UPDATE STATUS SUCCESS')

        # Append to the state database

        stateDb[chosenMemory['title']] = {"tweet_id":twitterPostData['id'], "posted_on":datetime.now().isoformat()}

        gist.edit(files={"state.json": github.InputFileContent(content=json.dumps(stateDb, indent=2))})
    else:
        print('UPDATE STATUS FAILURE: ' + r.text)