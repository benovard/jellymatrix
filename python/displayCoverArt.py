import time
import sys
import os
import configparser
import requests
from io import BytesIO
from PIL import Image
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from getSongInfo import getSongInfo

# Configuration file
dir = os.path.dirname(__file__)
filename = os.path.join(dir, '../config/rgb_options.ini')

# Configuration for the matrix
config = configparser.ConfigParser()
config.read(filename)

options = RGBMatrixOptions()
options.rows = int(config['DEFAULT']['rows'])
options.cols = int(config['DEFAULT']['columns'])
options.chain_length = int(config['DEFAULT']['chain_length'])
options.parallel = int(config['DEFAULT']['parallel'])
options.hardware_mapping = config['DEFAULT']['hardware_mapping']
options.gpio_slowdown = int(config['DEFAULT']['gpio_slowdown'])
options.brightness = int(config['DEFAULT']['brightness'])
options.limit_refresh_rate_hz = int(config['DEFAULT']['refresh_rate'])

default_image = os.path.join(dir, config['DEFAULT']['default_image'])
matrix = RGBMatrix(options = options)

prevSong    = ""
currentSong = ""

try:
  while True:
    try:
      imageURL = getSongInfo()
      currentSong = imageURL

      if ( prevSong != currentSong ):
        if imageURL is None:
          image = Image.open(default_image)
        else:
          response = requests.get(imageURL, timeout=5)
          image = Image.open(BytesIO(response.content))
        image.thumbnail((matrix.width, matrix.height), Image.Resampling.LANCZOS)
        matrix.SetImage(image.convert('RGB'))
        prevSong = currentSong

      time.sleep(1)
    except Exception as e:
      image = Image.open(default_image)
      image.thumbnail((matrix.width, matrix.height), Image.Resampling.LANCZOS)
      matrix.SetImage(image.convert('RGB'))
      print(e)
      time.sleep(1)
except KeyboardInterrupt:
  sys.exit(0)
