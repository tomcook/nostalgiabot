#!/usr/local/bin/python3

import os
import sys
import json
import shutil
import pathlib
import requests
from pprint import pprint

destinationDirectory = "photos/whitehouse/"
bucketingDigits      = 3

with open('memories-whitehouse-raw.json') as f:
  memories = json.load(f)

print(f" : Loaded memories DB with {len(memories)} memories")

for memory in memories:

    filename  = memory['url_o'].split('/')[-1]
    bucketing = filename[:bucketingDigits]

    finalDestination = f"{destinationDirectory}/{bucketing}/{filename}"

    print(finalDestination)

    pathlib.Path(f"{destinationDirectory}/{bucketing}").mkdir(parents=True, exist_ok=True)

    response = requests.get(memory['url_o'], stream=True)

    with open(finalDestination, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)

