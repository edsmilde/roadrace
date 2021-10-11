
from PIL import Image, ImageDraw
import math
import random




SIZE=(500, 700)

START=(250, SIZE[1]-100)

def radians(degrees):
    return degrees/180*math.pi


def sortAngleHelper(angle):
    return getAngleDistance(angle, radians(-90))


def getAngleDistance(angleA, angleB):
    distance = angleA - angleB
    if distance < 0:
        distance = -distance
    if distance > 2*math.pi:
        distance = distance % 2*math.pi
    if distance > math.pi:
        distance = 2*math.pi - distance
    return distance




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


def randRangeFloat(min, max):
    diff = max-min
    randPart = random.random()*diff
    return (min + randPart)

def randRangeFloatArray(arr):
    return randRangeFloat(arr[0], arr[1])


def interpolateArc(p1, p2, arcSize, ratio):
    bottomPoint = interpolate(p1, p2, ratio)
    parabolicRatio = 4*(ratio - ratio*ratio)
    arc = arcSize * parabolicRatio
    point = (bottomPoint[0], bottomPoint[1] + arc)
    return point

def interpolateArcScalar(arcSize, ratio):
    parabolicRatio = 4*(ratio - ratio*ratio)
    return arcSize * parabolicRatio

def getBoundariesForCircle(center, diameter):
    radius = diameter/2
    x1 = center[0] - radius
    x2 = center[0] + radius
    y1 = center[1] - radius
    y2 = center[1] + radius
    return (x1, y1, x2, y2)

def drawCircle(center, diameter, color, draw : ImageDraw.ImageDraw):
    xy = getBoundariesForCircle(center, diameter)
    draw.ellipse(xy, fill=color)
    return

numToDraw = 30

OUTPUT_PATH = "sprites/objects/trees/"

STUMP_START_WIDTH_RANGE = [12, 16]
HEIGHT_RANGE = [400, 550]
STUMP_DECAY_RATIO = 0.995
RESOLUTION = 5

BRANCH_START_LENGTH_RANGE = [100, 120]
BRANCH_DECAY_RATIO = 0.995

VERT_RATIO = 1/math.sqrt(3)

STUMP_COLOR = (100, 60, 20, 255)

BRANCH_ARC_RATIO = 0.2

BRANCH_COLOR = (0, 90, 40, 255)
BRANCH_COLOR_DEVIATION = 10
BRANCH_WIDTH = 1

SHADOW_OFFSET = 2

SUB_BRANCH_RATIO = 0.5

def drawBranch(start, length, angle, draw : ImageDraw.ImageDraw):
    endX = start[0] + math.cos(angle)*length
    endY = start[1] + math.sin(angle)*length*VERT_RATIO
    end = (endX, endY)
    arcSize = BRANCH_ARC_RATIO * length
    numPieces = int(length/RESOLUTION)
    color = getRandomColorDeviation(BRANCH_COLOR, BRANCH_COLOR_DEVIATION)
    shadowColor = interpolateColor(color, (0, 0, 0, 255), 0.5)
    angleSubBranchLeft = angle - radians(45)
    angleSubBranchRight = angle + radians(45)
    subBranchMaxLength = length * SUB_BRANCH_RATIO
    for i in range(numPieces):
        ratio = i/numPieces
        nextRatio = (i+1)/numPieces
        segmentStart = interpolateArc(start, end, arcSize, ratio)
        segmentEnd = interpolateArc(start, end, arcSize, nextRatio)
        shadowStart = (segmentStart[0], segmentStart[1]+SHADOW_OFFSET)
        shadowEnd = (segmentEnd[0], segmentEnd[1]+SHADOW_OFFSET)
        subBranchLength = interpolateArcScalar(subBranchMaxLength, ratio)
        subBranchLeftEndX = segmentEnd[0] + math.cos(angleSubBranchLeft)*subBranchLength
        subBranchLeftEndY = segmentEnd[1] + math.sin(angleSubBranchLeft)*subBranchLength*VERT_RATIO
        subBranchRightEndX = segmentEnd[0] + math.cos(angleSubBranchRight)*subBranchLength
        subBranchRightEndY = segmentEnd[1] + math.sin(angleSubBranchRight)*subBranchLength*VERT_RATIO
        subBranchLeftEnd = (subBranchLeftEndX, subBranchLeftEndY)
        subBranchRightEnd = (subBranchRightEndX, subBranchRightEndY)
        subBranchLeftShadowEnd = (subBranchLeftEndX, subBranchLeftEndY + SHADOW_OFFSET)
        subBranchRightShadowEnd = (subBranchRightEndX, subBranchRightEndY + SHADOW_OFFSET)
        draw.line((shadowStart, shadowEnd), fill=shadowColor, width=BRANCH_WIDTH)
        draw.line((shadowStart, subBranchLeftShadowEnd), fill=shadowColor, width=BRANCH_WIDTH)
        draw.line((shadowStart, subBranchRightShadowEnd), fill=shadowColor, width=BRANCH_WIDTH)
        draw.line((segmentStart, segmentEnd), fill=color, width=BRANCH_WIDTH)
        draw.line((segmentStart, subBranchLeftEnd), fill=color, width=BRANCH_WIDTH)
        draw.line((segmentStart, subBranchRightEnd), fill=color, width=BRANCH_WIDTH)


    return

ANGLE_SPREAD_RATIO = 2
def drawBranches(start, n, lengthRange, draw : ImageDraw.ImageDraw):
    angleSeeds = []
    angleSeedsSum = 0
    for i in range(n):
        angleSeed = randRangeFloat(1, ANGLE_SPREAD_RATIO)
        angleSeeds.append(angleSeed)
        angleSeedsSum += angleSeed
    nextAngle = randRangeFloat(0, 2*math.pi)
    angles = []
    for seed in angleSeeds:
        nextAngle += seed/angleSeedsSum*2*math.pi % (2*math.pi)
        angles.append(nextAngle)
    angles.sort(key=sortAngleHelper)
    for angle in angles:
        length = randRangeFloatArray(lengthRange)
        drawBranch(start, length, angle, draw)
    return

BRANCH_SPACE = 20

BRANCH_N = 6

def drawTree(draw : ImageDraw.ImageDraw):
    stumpWidth = randRangeFloatArray(STUMP_START_WIDTH_RANGE)
    height = randRangeFloatArray(HEIGHT_RANGE)
    location = START
    heightSoFar = 0
    lastBranch = 0
    branchRatio = 1
    while True:
        drawCircle(location, stumpWidth, STUMP_COLOR, draw)
        location = (location[0], location[1] - RESOLUTION)
        stumpWidth = randRangeFloat(stumpWidth*STUMP_DECAY_RATIO, stumpWidth)
        if lastBranch >= BRANCH_SPACE:
            nBranches = random.randrange(4, 8)
            branchRange = [BRANCH_START_LENGTH_RANGE[0]*branchRatio, BRANCH_START_LENGTH_RANGE[1]*branchRatio]
            drawBranches(location, nBranches, branchRange, draw)
            lastBranch = 0
        heightSoFar += RESOLUTION
        lastBranch += RESOLUTION
        branchRatio *= BRANCH_DECAY_RATIO
        if heightSoFar > height:
            break



OUTPUT_PATH = "sprites/objects/trees/"
NUM_TREES = 30


for i in range(NUM_TREES):
    image = Image.new('RGBA', SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    drawTree(draw)
    filename = OUTPUT_PATH + "evergreen_" + str(i) + ".png"
    image.save(filename, "PNG")







