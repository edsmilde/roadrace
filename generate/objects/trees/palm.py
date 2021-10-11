from PIL import Image, ImageDraw
import math
import random




SIZE=(500, 700)

START=(250, SIZE[1]-50)

def radians(degrees):
    return degrees/180*math.pi

def getAngleDistance(angleA, angleB):
    distance = angleA - angleB
    if distance < 0:
        distance = -distance
    if distance > 2*math.pi:
        distance = distance % 2*math.pi
    if distance > math.pi:
        distance = 2*math.pi - distance
    return distance


def getDistance(p1, p2):
    x = p2[0] - p1[0]
    y = p2[1] - p1[1]
    return math.sqrt(x*x + y*y)

def interpolateScalar(s1, s2, ratio):
    return (s1*(1-ratio) + s2*ratio)

def interpolate(p1, p2, ratio):
    x = p1[0] * (1-ratio) + p2[0] * ratio
    y = p1[1] * (1-ratio) + p2[1] * ratio
    return [x, y]

def interpolateArc(p1, p2, arcSize, ratio):
    bottomPoint = interpolate(p1, p2, ratio)
    parabolicRatio = 4*(ratio - ratio*ratio)
    arc = arcSize * parabolicRatio
    point = [bottomPoint[0], bottomPoint[1] + arc]
    return point

def randRangeFloat(min, max):
    diff = max-min
    randPart = random.random()*diff
    return (min + randPart)


def getRandomColorFromRange(colorA, colorB):
    red = random.randrange(colorA[0], colorB[0]+1)
    green = random.randrange(colorA[1], colorB[1]+1)
    blue = random.randrange(colorA[2], colorB[2]+1)
    alpha = random.randrange(colorA[3], colorB[3]+1)
    return (red, green, blue, alpha)


STEM_COLOR_MIN = (110, 70, 0, 255)
STEM_COLOR_MAX = (130, 90, 0, 255)
LEAF_COLOR_MIN = (0, 140, 40, 255)
LEAF_COLOR_MAX = (0, 160, 60, 255)

STEM_WIDTH_MAX = 20
STEM_WIDTH_MIN = 10
STEM_DECAY_RATIO = 0.98

RESOLUTION = 3

ANGLE_DECAY_RATIO = 0.97

HEIGHT_MIN = 400
HEIGHT_MAX = 550

DEPTH_RATIO = 1/math.sqrt(3)

NUM_LEAVES = 10
LEAVES_MIN_ANGLE_DISTANCE = radians(20)

LEAF_SIZE_MIN = 120
LEAF_SIZE_MAX = 160
LEAF_ARC_RATIO = -5000
LEAF_DROP_RATIO = 1.2

def drawCircle(center, diameter, draw : ImageDraw.ImageDraw, color):
    x1 = center[0] - diameter/2
    y1 = center[1] - diameter/2
    x2 = center[0] + diameter/2
    y2 = center[1] + diameter/2
    points = (x1, y1, x2, y2)
    draw.ellipse(points, fill=color)

# def sortAngleHelper(angleA, angleB):
#     distA = getAngleDistance(angleA, radians(90))
#     distB = getAngleDistance(angleB, radians(90))
#     return distA - distB

def sortAngleHelper(angle):
    return getAngleDistance(angle, radians(-90))

def drawTree(startPoint, draw : ImageDraw.ImageDraw):
    stemColor = getRandomColorFromRange(STEM_COLOR_MIN, STEM_COLOR_MAX)
    stemHeight = randRangeFloat(HEIGHT_MIN, HEIGHT_MAX)
    
    nextAngle = randRangeFloat(radians(-70), radians(-110))
    nextStemWidth = STEM_WIDTH_MAX
    nextStemX = startPoint[0]
    nextStemY = startPoint[1]
    stemPieces = int(stemHeight / RESOLUTION)

    for i in range(stemPieces + 1):
        center = [nextStemX, nextStemY]
        drawCircle(center, nextStemWidth, draw, stemColor)
        nextStemWidth = randRangeFloat(nextStemWidth, nextStemWidth * STEM_DECAY_RATIO)
        if nextStemWidth < STEM_WIDTH_MIN:
            nextStemWidth = STEM_WIDTH_MIN
        nextStemY = nextStemY + math.sin(nextAngle) * RESOLUTION
        nextStemX = nextStemX + math.cos(nextAngle) * RESOLUTION
        nextAngle = randRangeFloat(nextAngle, interpolateScalar(radians(-90), nextAngle, ANGLE_DECAY_RATIO))

    leafAngles = []

    for i in range(NUM_LEAVES):
        nextLeafAngle = 0
        while True:
            nextLeafAngle = randRangeFloat(0, radians(360))
            leafAngleValid = True
            for leafAngle in leafAngles:
                if getAngleDistance(leafAngle, nextLeafAngle) < LEAVES_MIN_ANGLE_DISTANCE:
                    leafAngleValid = False
                    break
            if leafAngleValid:
                leafAngles.append(nextLeafAngle)
                break

    leafAngles.sort(key=sortAngleHelper)

    leafStart = [nextStemX, nextStemY]


    for leafAngle in leafAngles:
        leafSize = randRangeFloat(LEAF_SIZE_MIN, LEAF_SIZE_MAX)
        leafArcSize = LEAF_ARC_RATIO / leafSize
        leafEndX = leafStart[0] + math.cos(leafAngle) * leafSize
        leafEndY = leafStart[1] + math.sin(leafAngle) * leafSize * DEPTH_RATIO
        leafEnd = [leafEndX, leafEndY]
        numPoints = int(leafSize / RESOLUTION)
        leafColor = getRandomColorFromRange(LEAF_COLOR_MIN, LEAF_COLOR_MAX)
        for i in range(numPoints + 1):
            ratio = i / numPoints
            belowPoint = interpolate(leafStart, leafEnd, ratio)
            topPoint = interpolateArc(leafStart, leafEnd, leafArcSize, ratio)
            bottomPoint = interpolate(topPoint, belowPoint, LEAF_DROP_RATIO)
            leafDropSize = getDistance(topPoint, bottomPoint)
            # drawCircle(topPoint, RESOLUTION, draw, LEAF_COLOR_MIN)
            numLeafDropPoints = int(leafDropSize / RESOLUTION)
            if numLeafDropPoints == 0:
                numLeafDropPoints = 1
            for j in range(numLeafDropPoints + 1):
                leafRatio = j / numLeafDropPoints
                point = interpolate(topPoint, bottomPoint, leafRatio)
                drawCircle(point, RESOLUTION*2, draw, leafColor)
        



    return






OUTPUT_PATH = "sprites/objects/trees/"

NUM_TREES = 30

for i in range(NUM_TREES):
    myImage = Image.new('RGBA', SIZE, (0, 0, 0, 0))
    myDraw = ImageDraw.Draw(myImage)
    drawTree(START, myDraw)
    filename = OUTPUT_PATH + "palm_" + str(i) + ".png"
    myImage.save(filename, "PNG")

        




