from PIL import Image, ImageDraw
import math
import random

HEIGHT=400
WIDTH=400

SIZE = (WIDTH, HEIGHT)

COLUMNS = 8
COLUMN_WIDTH = WIDTH/COLUMNS


def getRandomColorFromRange(colorA, colorB):
    red = random.randrange(colorA[0], colorB[0]+1)
    green = random.randrange(colorA[1], colorB[1]+1)
    blue = random.randrange(colorA[2], colorB[2]+1)
    alpha = random.randrange(colorA[3], colorB[3]+1)
    return (red, green, blue, alpha)

WOOD_COLOR_MIN = (210, 150, 100, 255)
WOOD_COLOR_MAX = (220, 160, 110, 255)

def getRandomVarationFromColor(color, variation):
    red = random.randrange(color[0]-variation, color[0]+variation)
    green = random.randrange(color[1]-variation, color[1]+variation)
    blue = random.randrange(color[2]-variation, color[2]+variation)
    rgb = [red, green, blue]
    for i in range(len(rgb)):
        if rgb[i] > 255:
            rgb[i] = 255
        if rgb[i] < 0:
            rgb[i] = 0
    alpha = color[3]
    return (rgb[0], rgb[1], rgb[2], alpha)

def getRandomWoodColor():
    return getRandomColorFromRange(WOOD_COLOR_MIN, WOOD_COLOR_MAX)


BACKGROUND_COLOR = (40, 20, 0, 255)

myImage = Image.new('RGBA', SIZE, BACKGROUND_COLOR)
myDraw = ImageDraw.Draw(myImage)

PADDING = 2

SPLIT_COLUMN = 5

COLOR_VARIANCE = 5

for i in range(COLUMNS):
    left = i*COLUMN_WIDTH + PADDING
    right = left + COLUMN_WIDTH - 2*PADDING
    color = getRandomWoodColor()
    innerWidth = right - left
    innerSplitWidth = innerWidth/SPLIT_COLUMN
    for i in range(SPLIT_COLUMN):
        innerLeft = left + i*innerSplitWidth
        innerRight = innerLeft + innerSplitWidth
        innerColor = getRandomVarationFromColor(color, COLOR_VARIANCE)
        myDraw.rectangle((innerLeft, 0, innerRight, HEIGHT), fill=innerColor)

    


OUTPUT_DIRECTORY = "sprites/ground/"
BASE_NAME = "plank"

myImage.save(OUTPUT_DIRECTORY + BASE_NAME + "_center.png", "PNG")

