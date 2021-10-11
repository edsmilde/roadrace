
from PIL import Image, ImageDraw
import math
import random

HEIGHT=1200
WIDTH=1200


OVERFLOW_SIZE = 20 # int(SIDE_MAX/2)



images = {}
draws = {}
offsets = {}

images['center'] = Image.new('RGBA', (WIDTH, HEIGHT), (0, 60, 0, 255))
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




RED_MIN=0
RED_MAX=30
GREEN_MIN=120
GREEN_MAX=190
BLUE_MIN=0
BLUE_MAX=60

class Piece:
  def __init__(self, baseX=0, baseY=0, length=0, width=0, angle=0):
    self.baseX = baseX
    self.baseY = baseY
    self.length = length
    self.width = width
    self.angle = angle
    self.color = (
      random.randrange(RED_MIN, RED_MAX),
      random.randrange(GREEN_MIN, GREEN_MAX),
      random.randrange(BLUE_MIN, BLUE_MAX)
    )
    
  
  def draw(self, drawer):
    endX = self.baseX + self.length*math.cos(self.angle)
    endY = self.baseY - self.length*math.sin(self.angle)
    drawer.line(((self.baseX, self.baseY), (endX, endY)), width=self.width, fill=self.color)
  
  def getShifted(self, x, y):
    pieceShifted = Piece()
    pieceShifted.baseX = self.baseX + x
    pieceShifted.baseY = self.baseY + y
    pieceShifted.length = self.length
    pieceShifted.width = self.width
    pieceShifted.color = self.color
    pieceShifted.angle = self.angle
    return pieceShifted
  
  def getLeft(self):
    return min(self.baseX, self.baseX + self.length*math.cos(self.angle))
  
  def getRight(self):
    return max(self.baseX, self.baseX + self.length*math.cos(self.angle))
  
  def getTop(self):
    return self.baseY - self.length*math.sin(self.angle)
  
  def getBottom(self):
    return self.baseY
    

def radians(degrees):
  return degrees/180*math.pi


MAX_PIECE_LENGTH=30
MIN_PIECE_LENGTH=15
MAX_PIECE_WIDTH=6
MIN_PIECE_WIDTH=2

for i in range(HEIGHT+1):
  thisBaseY = i
  for j in range(30):
    thisBaseX = random.randrange(WIDTH+1)
    thisLength = random.randrange(MIN_PIECE_LENGTH, MAX_PIECE_LENGTH)
    thisWidth = random.randrange(MIN_PIECE_WIDTH, MAX_PIECE_WIDTH)
    
    thisAngle = radians(60 + random.random()*60)
    
    thisPiece = Piece(thisBaseX, thisBaseY, thisLength, thisWidth, thisAngle)
    
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
    
          
    
  
  
BASE_NAME="grass"

for imageKey in images:
  images[imageKey].save("sprites/ground/" + BASE_NAME + "_" + imageKey + ".png")

    
  



