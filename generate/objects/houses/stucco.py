from PIL import Image, ImageDraw
import math
import random

HEIGHT=500
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



WALL_COLOR = (225, 215, 205, 255)



ROOF_COLOR_MIN = (140, 70, 40, 255)
ROOF_COLOR_MAX = (160, 90, 60, 255)

def interpolateColor(colorA, colorB, ratio):
    rgba = []
    for i in range(4):
        color = int(colorA[i] * (1-ratio) + colorB[i] * ratio)
        rgba.append(color)
    return (rgba[0], rgba[1], rgba[2], rgba[3])

def interpolateColorTuple(colorA, colorB, ratio):
    rgba = []
    for i in range(4):
        color = int(colorA[i] * (1-ratio[i]) + colorB[i] * ratio[i])
        rgba.append(color)
    return (rgba[0], rgba[1], rgba[2], rgba[3])



def drawRoof(left, right, top, bottom, wavelength, resolution, draw : ImageDraw.ImageDraw):
    width = right - left
    n = int(width / resolution)
    for i in range(n):
        pieceLeft = i * resolution
        phase = (pieceLeft % wavelength) / wavelength * 2 * math.pi
        ratio = (math.sin(phase) + 1) / 2
        color = interpolateColor(ROOF_COLOR_MIN, ROOF_COLOR_MAX, ratio)
        drop = ratio * wavelength / math.pi
        pieceBottom = bottom + drop
        pieceRight = pieceLeft + resolution
        draw.rectangle((pieceLeft, top, pieceRight, pieceBottom), fill=color)
    return

ROOF_SIZE = 200

class DiscolorationMatrix:
    def __init__(self, width : int, height : int, blur) -> None:
        self.matrix = []
        for i in range(width):
            col = []
            for j in range(height):
                col.append(0)
            self.matrix.append(col)
        factor = blur * blur
        for i in range(width):
            for j in range(height):
                seed = random.random() / factor
                for k in range(blur):
                    for m in range(blur):
                        thisCol = (i + k) % width
                        thisRow = (j + m) % height
                        self.matrix[thisCol][thisRow] += seed
    def draw(self, x, y, image : ImageDraw.ImageDraw):
        return
    def get(self, x, y):
        return self.matrix[x][y]

redDiscolorationMatrix = DiscolorationMatrix(200, 400, 20)
greenDiscolorationMatrix = DiscolorationMatrix(200, 400, 20)
blueDiscolorationMatrix = DiscolorationMatrix(200, 400, 20)


def getHouseBase():
    image = Image.new('RGBA', SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, ROOF_SIZE, WIDTH, HEIGHT), fill=WALL_COLOR)
    drawRoof(0, WIDTH, 0, ROOF_SIZE, 20, 2, draw)
    return image, draw


OUTPUT_DIRECTORY = "sprites/objects/buildings/"
BASE_NAME = "stucco"

def savePiece(image : Image.Image , piece):
    filename = OUTPUT_DIRECTORY + BASE_NAME + "_" + piece + ".png"
    image.save(filename, "PNG")

# Plain
imageBlank, drawBlank = getHouseBase()
savePiece(imageBlank, "blank")

# Left edge
imageLeft, drawLeft = getHouseBase()
drawLeft.polygon((0, 0, WIDTH, 0, 0, ROOF_SIZE), fill=(0, 0, 0, 0))
savePiece(imageLeft, "left")

# Right edge
imageRight, drawRight = getHouseBase()
drawRight.polygon((0, 0, WIDTH, ROOF_SIZE, WIDTH, 0), fill=(0, 0, 0, 0))
savePiece(imageRight, "right")


def drawArc(x, y, width, radius, color, draw : ImageDraw.ImageDraw):
    centerY = y + math.sqrt(radius*radius - width*width/4)
    arcBounds = (x - radius, centerY - radius, x + radius, centerY + radius)
    angleStart = -90-degrees(math.asin(width/2/radius))
    angleEnd = -90+degrees(math.asin(width/2/radius))
    draw.chord(arcBounds, angleStart, angleEnd, fill=color)

# Window

imageWindow, drawWindow = getHouseBase()
shadowColor = interpolateColor(WALL_COLOR, (0, 0, 0, 255), 0.2)

windowHeight = 150
windowBottom = 420
windowWidth = 120

windowLeft = (WIDTH - windowWidth) / 2
windowRight = (WIDTH + windowWidth) / 2
windowTop = windowBottom - windowHeight

arcRadius = 100

drawArc(WIDTH/2, windowTop, windowWidth, arcRadius, shadowColor, drawWindow)
drawWindow.rectangle((windowLeft, windowTop, windowRight, windowBottom), fill=shadowColor)

paneColor = (20, 20, 50, 255)
windowPadding = 10
paneRadius=3
drawWindow.rounded_rectangle((windowLeft+windowPadding, windowTop+windowPadding, windowRight-windowPadding, windowBottom-windowPadding), fill=paneColor, radius=paneRadius)

savePiece(imageWindow, "window")

# Door

imageDoor, drawDoor = getHouseBase()

doorHeight = 230
doorTop = HEIGHT - doorHeight
doorWidth = 120
arcRadius = 100

drawArc(WIDTH/2, doorTop, doorWidth, arcRadius, shadowColor, drawDoor)

doorLeft = (WIDTH - doorWidth)/2
doorRight = (WIDTH + doorWidth)/2
drawDoor.rectangle((doorLeft, doorTop, doorRight, HEIGHT), fill=shadowColor)

innerWidth = 100
innerHeight = 220

innerSegments = 10
innerSegmentWidth = innerWidth/innerSegments

for i in range(innerSegments):
    segmentLeft = (WIDTH-innerWidth)/2 + i*innerSegmentWidth
    segmentRight = segmentLeft + innerSegmentWidth
    segmentColor = getRandomColorFromRange(WOOD_COLOR_MIN, WOOD_COLOR_MAX)
    outlineColor = interpolateColor(segmentColor, (0, 0, 0, 255), 0.1)
    drawDoor.rectangle((segmentLeft, HEIGHT-innerHeight, segmentRight, HEIGHT), fill=segmentColor, outline=outlineColor, width=1)

savePiece(imageDoor, "door")






