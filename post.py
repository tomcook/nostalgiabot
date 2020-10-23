import os
import json
import github
import shutil
import random
import requests
from datetime import datetime
from TwitterAPI import TwitterAPI

stateDbGist = 'd34ccb38adf1b9ec9366b892b3e40ae6'
memoryDbUrl = 'https://raw.githubusercontent.com/tomcook/nostalgiabot-obama/main/memories.json'

githubToken = os.environ.get('GIST_TOKEN')

api = TwitterAPI(os.environ.get('TWITTER_CONSUMER_KEY'), 
                 os.environ.get('TWITTER_CONSUMER_SECRET'),
                 os.environ.get('TWITTER_ACCESS_TOKEN_KEY'),
                 os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'))

# Get the GitHub Gist that contains our state database
gh = github.Github(githubToken)
gist = gh.get_gist(stateDbGist)

stateDb = json.loads(gist.files['state.json'].content)

# Get the memories DB

req = requests.get(memoryDbUrl)
memories = req.json()

# Find our random memory to post from the DB

chosenMemory = random.choice(memories)

print(chosenMemory)

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
    if r.status_code == 200 
        print('UPDATE STATUS SUCCESS')

        # Append to the state database

        stateDb[chosenMemory['title']] = {"tweet_id":r.text['id'], "posted_on":r.text['created_at']}

        gist.edit(files={"state.json": github.InputFileContent(content=json.dumps(stateDb))})
    else:
        print('UPDATE STATUS FAILURE: ' + r.text)