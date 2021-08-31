from PIL import Image, ImageDraw
import math
import random

HEIGHT=400
WIDTH=400

SIZE = (WIDTH, HEIGHT)

ROWS = 12
RATIO = 2


def getRandomColorFromRange(colorA, colorB):
    red = random.randrange(colorA[0], colorB[0]+1)
    green = random.randrange(colorA[1], colorB[1]+1)
    blue = random.randrange(colorA[2], colorB[2]+1)
    alpha = random.randrange(colorA[3], colorB[3]+1)
    return (red, green, blue, alpha)

BRICK_COLOR_MIN = (100, 20, 0, 255)
BRICK_COLOR_MAX = (140, 50, 20, 255)

def getRandomBrickColor():
    return getRandomColorFromRange(BRICK_COLOR_MIN, BRICK_COLOR_MAX)


BACKGROUND_COLOR = (150, 150, 150, 255)

myImage = Image.new('RGBA', SIZE, BACKGROUND_COLOR)
myDraw = ImageDraw.Draw(myImage)

brickHeight = HEIGHT/ROWS
brickWidth = brickHeight * RATIO
bricksPerRow = int(ROWS / RATIO)

CORNER_RADIUS = 4
PADDING = 2

for i in range(ROWS):
    top = i * brickHeight + PADDING
    for j in range(bricksPerRow):
        left = 0
        if (i % 2) == 0:
            left = j * brickWidth + PADDING
        else:
            left = (j - 0.5) * brickWidth + PADDING
        right = left + brickWidth - 2*PADDING
        bottom = top + brickHeight - 2*PADDING
        color = getRandomBrickColor()
        myDraw.rounded_rectangle((left, top, right, bottom), fill=color, radius=CORNER_RADIUS)
        if (i % 2) == 1 and j == 0:
            myDraw.rounded_rectangle((left + WIDTH, top, right + WIDTH, bottom), fill=color, radius=CORNER_RADIUS)






OUTPUT_DIRECTORY = "sprites/ground/"
BASE_NAME = "brick"

myImage.save(OUTPUT_DIRECTORY + BASE_NAME + "_center.png", "PNG")

