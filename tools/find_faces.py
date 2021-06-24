#!/usr/local/bin/python3

import json
import face_recognition

with open('memories.json') as f:
  memories = json.load(f)

print(f" : Loaded memories DB with {len(memories)} memories")

for memory in memories:

    filename  = memory['photo_url'].split('raw/main/')[1]
    
    image = face_recognition.load_image_file(filename)
    face_locations = face_recognition.face_locations(image)

    if len(face_locations) > 0:
      print(f"{filename}: {len(face_locations)}")
    else:
      print(filename)
