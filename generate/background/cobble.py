
from PIL import Image, ImageDraw
import math
import random

HEIGHT=400
WIDTH=400

SIDE_MIN=20
SIDE_MAX=40

OVERFLOW_SIZE = 40

THICKNESS=3

DARK_MAX=95
DARK_MIN=65

LIGHT_MAX=145
LIGHT_MIN=115


def getRandomColorFromRange(colorA, colorB):
    red = random.randrange(colorA[0], colorB[0]+1)
    green = random.randrange(colorA[1], colorB[1]+1)
    blue = random.randrange(colorA[2], colorB[2]+1)
    alpha = random.randrange(colorA[3], colorB[3]+1)
    return (red, green, blue, alpha)

STONE_COLOR_MIN = (90, 60, 60, 255)
STONE_COLOR_MAX = (110, 80, 80, 255)

CEMENT_COLOR_MIN = (150, 130, 140, 255)
CEMENT_COLOR_MAX = (160, 140, 150, 255)

def getRandomStoneColor():
    return getRandomColorFromRange(STONE_COLOR_MIN, STONE_COLOR_MAX)

def getRandomCementColor():
    return getRandomColorFromRange(CEMENT_COLOR_MIN, CEMENT_COLOR_MAX)




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

offsetsBorder = [
  (0, 0),
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


def drawWithOffset(corners, offset, draw, color):
  cornersWithOffset = shiftCorners(corners, offset)
  draw.ellipse(cornersWithOffset, fill=color)

def drawWithDoubleOffset(corners, offset1, offset2, draw, color):
  cornersWithOffset = shiftCorners(corners, offset1)
  drawWithOffset(cornersWithOffset, offset2, draw, color)

class Piece:
  def __init__(self, centerX=0, centerY=0, outerWidth=0, outerHeight=0):
    self.centerX = centerX
    self.centerY = centerY
    self.outerHeight = outerHeight
    self.outerWidth = outerWidth
    self.innerColor = getRandomStoneColor()
    self.outerColor = getRandomCementColor()
  
  def draw(self, drawer):
    innerWidth = self.outerWidth - THICKNESS*2
    innerHeight = self.outerHeight - THICKNESS*2
    outerTopLeft = (self.centerX - self.outerWidth/2, self.centerY - self.outerHeight/2)
    outerBottomRight = (self.centerX + self.outerWidth/2, self.centerY + self.outerHeight/2)
    innerTopLeft = (self.centerX - innerWidth/2, self.centerY - innerHeight/2)
    innerBottomRight = (self.centerX + innerWidth/2, self.centerY + innerHeight/2)
    outerCorners = (outerTopLeft, outerBottomRight)
    innerCorners = (innerTopLeft, innerBottomRight)
    drawer.ellipse(outerCorners, fill=self.outerColor)
    drawer.ellipse(innerCorners, fill=self.innerColor)
  
  def getShifted(self, x, y):
    pieceShifted = Piece()
    pieceShifted.centerX = self.centerX + x
    pieceShifted.centerY = self.centerY + y
    pieceShifted.outerHeight = self.outerHeight
    pieceShifted.outerWidth = self.outerWidth
    pieceShifted.innerColor = self.innerColor
    pieceShifted.outerColor = self.outerColor
    return pieceShifted
  
  def getLeft(self):
    return self.centerX - self.outerWidth/2
  
  def getRight(self):
    return self.centerX + self.outerWidth/2
  
  def getTop(self):
    return self.centerY - self.outerHeight/2
  
  def getBottom(self):
    return self.centerY + self.outerHeight/2
    

  

for j in range(10000):
  outerHeight = random.randrange(SIDE_MIN, SIDE_MAX)
  outerWidth = random.randrange(SIDE_MIN, SIDE_MAX)
  
  innerWidth = outerWidth - THICKNESS*2
  innerHeight = outerHeight - THICKNESS*2
  
  centerX = random.randrange(0, WIDTH+1)
  centerY = random.randrange(0, HEIGHT+1)
  
  thisPiece = Piece(centerX, centerY, outerWidth, outerHeight)
  
  thisPiece.draw(draws['center'])
  
  # left
  #
  if (thisPiece.getLeft() < 0):
    thisPiece.getShifted(WIDTH, 0).draw(draws['center'])
    thisPiece.getShifted(OVERFLOW_SIZE, 0).draw(draws['left'])
    thisPiece.draw(draws['right'])
    # top left
    #
    if (thisPiece.getTop() < 0):
      thisPiece.getShifted(OVERFLOW_SIZE, OVERFLOW_SIZE).draw(draws['topLeft'])
      thisPiece.getShifted(0, 0).draw(draws['bottomRight'])
      thisPiece.getShifted(OVERFLOW_SIZE, 0).draw(draws['bottomLeft'])
      thisPiece.getShifted(0, OVERFLOW_SIZE).draw(draws['topRight'])
    # bottom left
    #
    if (thisPiece.getBottom() > HEIGHT):
      thisPiece.getShifted(OVERFLOW_SIZE, -HEIGHT).draw(draws['bottomLeft'])
      thisPiece.getShifted(OVERFLOW_SIZE, -HEIGHT+OVERFLOW_SIZE).draw(draws['topLeft'])
      thisPiece.getShifted(0, -HEIGHT).draw(draws['bottomRight'])
      thisPiece.getShifted(0, -HEIGHT+OVERFLOW_SIZE).draw(draws['topRight'])
  # right
  #
  if (thisPiece.getRight() > WIDTH):
    thisPiece.getShifted(-WIDTH, 0).draw(draws['center'])
    thisPiece.getShifted(-WIDTH, 0).draw(draws['right'])
    thisPiece.getShifted(OVERFLOW_SIZE-WIDTH, 0).draw(draws['left'])
    # top right
    #
    if (thisPiece.getTop() < 0):
      thisPiece.getShifted(-WIDTH, OVERFLOW_SIZE).draw(draws['topRight'])
      thisPiece.getShifted(-WIDTH, 0).draw(draws['bottomRight'])
      thisPiece.getShifted(-WIDTH+OVERFLOW_SIZE, OVERFLOW_SIZE).draw(draws['topLeft'])
      thisPiece.getShifted(-WIDTH+OVERFLOW_SIZE, 0).draw(draws['bottomLeft'])
    # bottom right
    #
    if (thisPiece.getBottom() > HEIGHT):
      thisPiece.getShifted(-WIDTH, -HEIGHT).draw(draws['bottomRight'])
      thisPiece.getShifted(-WIDTH, -HEIGHT+OVERFLOW_SIZE).draw(draws['topRight'])
      thisPiece.getShifted(-WIDTH+OVERFLOW_SIZE, -HEIGHT+OVERFLOW_SIZE).draw(draws['topLeft'])
      thisPiece.getShifted(-WIDTH+OVERFLOW_SIZE, -HEIGHT).draw(draws['bottomLeft'])
  # top
  #
  if (thisPiece.getTop() < 0):
    thisPiece.getShifted(0, HEIGHT).draw(draws['center'])
    thisPiece.getShifted(0, OVERFLOW_SIZE).draw(draws['top'])
    thisPiece.draw(draws['bottom'])
  # bottom
  #
  if (thisPiece.getBottom() > HEIGHT):
    thisPiece.getShifted(0, -HEIGHT).draw(draws['center'])
    thisPiece.getShifted(0, -HEIGHT).draw(draws['bottom'])
    thisPiece.getShifted(0, OVERFLOW_SIZE-HEIGHT).draw(draws['top'])
    
          
    
  
  
BASE_NAME="cobble"

for imageKey in images:
  images[imageKey].save("sprites/ground/" + BASE_NAME + "_" + imageKey + ".png")

    
  



