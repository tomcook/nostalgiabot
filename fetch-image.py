import json
import shutil
import requests
from PIL import Image

with open('memory.json', 'r') as f:
    chosenMemory = json.load(f)

# Download the memory image

response = requests.get(chosenMemory['source'], stream=True)

with open('img.jpg', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)

# Resize image
img = Image.open('img.jpg')
img.save('img_resized.jpg', format="JPEG", quality=50)