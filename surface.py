
from PIL import Image, ImageDraw
import math
import random

HEIGHT=400
WIDTH=400

SIDE_MIN=10
SIDE_MAX=20

OVERFLOW_SIZE = int(SIDE_MAX/2)

THICKNESS=3

DARK_MAX=95
DARK_MIN=65

LIGHT_MAX=145
LIGHT_MIN=115


images = {}
draws = {}
offsets = {}

images['center'] = Image.new('RGBA', (WIDTH, HEIGHT), (DARK_MIN, DARK_MIN, DARK_MIN, 255))
images['top'] = Image.new('RGBA', (WIDTH, OVERFLOW_SIZE), (0, 0, 0, 0))
images['bottom'] = Image.new('RGBA', (WIDTH, OVERFLOW_SIZE), (0, 0, 0, 0))
images['left'] = Image.new('RGBA', (OVERFLOW_SIZE, HEIGHT), (0, 0, 0, 0))
images['right'] = Image.new('RGBA', (OVERFLOW_SIZE, HEIGHT), (0, 0, 0, 0))
images['topLeft'] = Image.new('RGBA', (OVERFLOW_SIZE, OVERFLOW_SIZE), (0, 0, 0, 0))
images['topRight'] = Image.new('RGBA', (OVERFLOW_SIZE, OVERFLOW_SIZE), (0, 0, 0, 0))
images['bottomLeft'] = Image.new('RGBA', (OVERFLOW_SIZE, OVERFLOW_SIZE), (0, 0, 0, 0))
images['bottomRight'] = Image.new('RGBA', (OVERFLOW_SIZE, OVERFLOW_SIZE), (0, 0, 0, 0))

offsets['center'] = (0, 0)
offsets['top'] = (0, -OVERFLOW_SIZE)
offsets['bottom'] = (0, HEIGHT)
offsets['left'] = (-OVERFLOW_SIZE, 0)
offsets['right'] = (WIDTH, 0)
offsets['topLeft'] = (-OVERFLOW_SIZE, -OVERFLOW_SIZE)
offsets['topRight'] = (WIDTH, -OVERFLOW_SIZE)
offsets['bottomLeft'] = (-OVERFLOW_SIZE, HEIGHT)
offsets['bottomRight'] = (WIDTH, HEIGHT)

offsetsCenter = [
  (WIDTH, 0),
  (0, HEIGHT),
  (WIDTH, HEIGHT)
]


for imageKey in images:
  draws[imageKey] = ImageDraw.Draw(images[imageKey])



def shiftPoint(point, delta):
  shiftedPoint = (point[0] - delta[0], point[1] - delta[1])
  return shiftedPoint


def shiftCorners(corners, delta):
  shiftedCorners = (shiftPoint(corners[0], delta), shiftPoint(corners[1], delta))
  return shiftedCorners

for j in range(10000):
  outerHeight = random.randrange(SIDE_MIN, SIDE_MAX)
  outerWidth = random.randrange(SIDE_MIN, SIDE_MAX)
  
  innerWidth = outerWidth - THICKNESS*2
  innerHeight = outerHeight - THICKNESS*2
  
  centerX = random.randrange(0, WIDTH+1)
  centerY = random.randrange(0, HEIGHT+1)
  
  outerTopLeft = (centerX - outerWidth/2, centerY - outerHeight/2)
  outerBottomRight = (centerX + outerWidth/2, centerY + outerHeight/2)
  
  innerTopLeft = (centerX - innerWidth/2, centerY - innerHeight/2)
  innerBottomRight = (centerX + innerWidth/2, centerY + innerHeight/2)
  
  lightShade = random.randrange(LIGHT_MIN, LIGHT_MAX)
  darkShade = random.randrange(DARK_MIN, DARK_MAX)
  
  lightColor = (lightShade, lightShade, lightShade, 255)
  darkColor = (darkShade, darkShade, darkShade, 255)
  
  outerCorners = (outerTopLeft, outerBottomRight)
  innerCorners = (innerTopLeft, innerBottomRight)
  
  for offsetKey in offsets:
    outerCornersOffset = shiftCorners(outerCorners, offsets[offsetKey])
    innerCornersOffset = shiftCorners(innerCorners, offsets[offsetKey])
    draws[offsetKey].ellipse(outerCornersOffset, fill=darkColor)
    draws[offsetKey].ellipse(innerCornersOffset, fill=lightColor)
  
  
  for offset in offsetsCenter:
    outerCornersOffset = shiftCorners(outerCorners, offset)
    innerCornersOffset = shiftCorners(innerCorners, offset)
    draws['center'].ellipse(outerCornersOffset, fill=darkColor)
    draws['center'].ellipse(innerCornersOffset, fill=lightColor)
  
  
    


for imageKey in images:
  images[imageKey].save("sprites/ground/asphalt_" + imageKey + ".png")

    
  



