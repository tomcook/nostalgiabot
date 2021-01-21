#!/usr/local/bin/python3
import os
import sys
import json
import flickrapi
from pprint import pprint

flickr_api_key    = os.environ.get('FLICKR_API_KEY')
flickr_api_secret = os.environ.get('FLICKR_API_SECRET')

flickrUserId = os.environ.get('FLICKR_USER_ID')
firstPage = 1

flickr = flickrapi.FlickrAPI(flickr_api_key, flickr_api_secret, format='parsed-json')

photoDb = []
fetchPage = firstPage

while True:

    print(f"Fetching page: {fetchPage}. Total records fetched: {len(photoDb)}")

    results = flickr.photos.search(user_id=flickrUserId, per_page='25', extras='description,url_o,url_m,url_l,date_taken,last_update', page=fetchPage)
    
    for item in results['photos']['photo']:
        photoDb.append(item)
    if fetchPage >= results['photos']['pages']:
        break
    else:
        fetchPage += 1

with open('memories-unprocessed.json', 'w') as outfile:
    json.dump(photoDb, outfile, indent=2)

    outfile.close()