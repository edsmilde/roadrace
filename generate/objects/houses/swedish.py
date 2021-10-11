from PIL import Image, ImageDraw
import math
import random

HEIGHT=400
WIDTH=200

SIZE = (WIDTH, HEIGHT)


def radians(degrees):
    return degrees/180*math.pi


def degrees(radians):
    return radians/math.pi*180

def getRandomColorFromRange(colorA, colorB):
    red = random.randrange(colorA[0], colorB[0]+1)
    green = random.randrange(colorA[1], colorB[1]+1)
    blue = random.randrange(colorA[2], colorB[2]+1)
    alpha = random.randrange(colorA[3], colorB[3]+1)
    return (red, green, blue, alpha)

WOOD_COLOR_MAX = (190, 130, 40, 255)
WOOD_COLOR_MIN = (180, 120, 30, 255)


# WALL_COLOR_MIN = (220, 210, 200, 255)
# WALL_COLOR_MAX = (230, 220, 210, 255)

# def getRandomWallColor():
#     return getRandomColorFromRange(WALL_COLOR_MIN, WALL_COLOR_MAX)



WALL_COLOR = (128, 24, 24, 255)



def interpolateColor(colorA, colorB, ratio):
    rgba = []
    for i in range(4):
        color = int(colorA[i] * (1-ratio) + colorB[i] * ratio)
        rgba.append(color)
    return (rgba[0], rgba[1], rgba[2], rgba[3])

def getRandomColorDeviation(color, variance):
    rgb = []
    for i in range(3):
        value = random.randrange(color[i]-variance, color[i]+variance)
        if value > 255:
            value = 255
        if value < 0:
            value = 0
        rgb.append(value)
    return (rgb[0], rgb[1], rgb[2], color[3])


SEGMENTS = 10
segmentWidth = WIDTH/SEGMENTS

def getHouseBase():
    image = Image.new('RGBA', SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    for i in range(SEGMENTS):
        segmentLeft = i*segmentWidth
        segmentRight = segmentLeft + segmentWidth
        color = getRandomColorDeviation(WALL_COLOR, 5)
        outlineColor = interpolateColor(color, (0, 0, 0, 255), 0.1)
        draw.rectangle((segmentLeft, 0, segmentRight, HEIGHT), fill=color, width=1, outline=outlineColor)
    return image, draw


OUTPUT_DIRECTORY = "sprites/objects/buildings/"
BASE_NAME = "swedish"

def savePiece(image : Image.Image , piece):
    filename = OUTPUT_DIRECTORY + BASE_NAME + "_" + piece + ".png"
    image.save(filename, "PNG")

# Plain
imageBlank, drawBlank = getHouseBase()
savePiece(imageBlank, "blank")

PANE_WIDTH = 20
PANE_COLOR = (230, 230, 230, 255)
# Left

imageLeft, drawLeft = getHouseBase()

drawLeft.rectangle((0, 0, WIDTH/2, HEIGHT), fill=(0, 0, 0, 0))

paneLeft = (WIDTH-PANE_WIDTH)/2
paneRight = (WIDTH+PANE_WIDTH)/2

drawLeft.rectangle((paneLeft, 0, paneRight, HEIGHT), fill=PANE_COLOR)

savePiece(imageLeft, "left")

# Right
imageRight, drawRight = getHouseBase()

drawRight.rectangle((WIDTH/2, 0, WIDTH, HEIGHT), fill=(0, 0, 0, 0))

paneLeft = (WIDTH-PANE_WIDTH)/2
paneRight = (WIDTH+PANE_WIDTH)/2

drawRight.rectangle((paneLeft, 0, paneRight, HEIGHT), fill=PANE_COLOR)

savePiece(imageRight, "right")


# Window
imageWindow, drawWindow = getHouseBase()

windowWidth = 150
windowHeight = 220
windowBottom = 330

windowLeft = (WIDTH-windowWidth)/2
windowRight = (WIDTH+windowWidth)/2
windowTop = windowBottom - windowHeight


drawWindow.rectangle((windowLeft, windowTop, windowRight, windowBottom), fill=PANE_COLOR)

windowColor = (20, 20, 60, 255)

drawWindow.rectangle((windowLeft+PANE_WIDTH, windowTop+PANE_WIDTH, windowRight-PANE_WIDTH, windowBottom-PANE_WIDTH), fill=windowColor)

innerPaneWidth = PANE_WIDTH/2

verticalPaneLeft = (WIDTH - innerPaneWidth)/2
verticalPaneRight = (WIDTH + innerPaneWidth)/2
drawWindow.rectangle((verticalPaneLeft, windowTop, verticalPaneRight, windowBottom), fill=PANE_COLOR)

horizontalPaneTop = windowBottom - (windowHeight+innerPaneWidth)/2
horizontalPaneBottom = horizontalPaneTop + innerPaneWidth

drawWindow.rectangle((windowLeft, horizontalPaneTop, windowRight, horizontalPaneBottom), fill=PANE_COLOR)




savePiece(imageWindow, "window")

# Door
imageDoor, drawDoor = getHouseBase()


doorHeight = 300
doorWidth = 150

doorTop = HEIGHT-doorHeight
doorLeft = (WIDTH-doorWidth)/2
doorRight = (WIDTH+doorWidth)/2


drawDoor.rectangle((doorLeft, doorTop, doorRight, HEIGHT), fill=PANE_COLOR)

doorColor = (80, 150, 200, 255)

drawDoor.rectangle((doorLeft+PANE_WIDTH, doorTop+PANE_WIDTH, doorRight-PANE_WIDTH, HEIGHT), fill=doorColor)


savePiece(imageDoor, "door")



