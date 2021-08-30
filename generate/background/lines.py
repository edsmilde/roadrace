
from PIL import Image, ImageDraw
import math
import random

HEIGHT=1600
WIDTH=80


# Start line

imageStartLine = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))

drawStartLine = ImageDraw.Draw(imageStartLine)

colorStartLine = (200, 200, 0, 255)
drawStartLine.rectangle([(0, 0), (WIDTH, HEIGHT)], fill=colorStartLine)

imageStartLine.save("sprites/lines/start.png")


# Finish line

CHECKER_SIZE = 20
CHECKER_COLS = int(WIDTH/CHECKER_SIZE-1) + 1
CHECKER_ROWS = int(HEIGHT/CHECKER_SIZE-1) + 1

imageFinishLine = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))

drawFinishLine = ImageDraw.Draw(imageFinishLine)


for i in range(CHECKER_COLS):
  for j in range(CHECKER_ROWS):
    isWhite = (i + j) % 2
    thisColor = (0, 0, 0, 255)
    if isWhite:
      thisColor = (255, 255, 255, 255)
    left = CHECKER_SIZE*i
    top = CHECKER_SIZE*j
    right = CHECKER_SIZE*(i+1)
    bottom = CHECKER_SIZE*(j+1)
    drawFinishLine.rectangle([(left, top), (right, bottom)], fill=thisColor)

imageFinishLine.save("sprites/lines/finish.png")

    
  



