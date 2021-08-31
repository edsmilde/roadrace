
from PIL import Image, ImageDraw
import math
import random




SIZE=(500, 700)

START=(250, SIZE[1]-50)

def radians(degrees):
    return degrees/180*math.pi

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

def getBoundariesForCircle(center, diameter):
    radius = diameter/2
    x1 = center[0] - radius
    x2 = center[0] + radius
    y1 = center[1] - radius
    y2 = center[1] + radius
    return (x1, y1, x2, y2)

BRANCH_COLOR = (60, 40, 0, 255)

class Branch:
    def __init__(self, startPoint, endPoint, startWidth, endWidth, color=BRANCH_COLOR):
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.startWidth = startWidth
        self.endWidth = endWidth
        self.color = color
    def draw(self, draw : ImageDraw.ImageDraw, resolution=1):
        length = getDistance(self.startPoint, self.endPoint)
        points = int(length/resolution)
        for i in range(points+1):
            ratio = i/points
            center = interpolate(self.startPoint, self.endPoint, ratio)
            width = interpolateScalar(self.startWidth, self.endWidth, ratio)
            ellipsePoints = getBoundariesForCircle(center, width)
            draw.ellipse(ellipsePoints, fill=self.color)
        return

LEAF_COLOR = (0, 180, 40, 100)

LEAF_COLOR_MIN = (0, 90, 15, 90)
LEAF_COLOR_MAX = (20, 110, 30, 110)

def getRandomColorFromRange(colorA, colorB):
    red = random.randrange(colorA[0], colorB[0]+1)
    green = random.randrange(colorA[1], colorB[1]+1)
    blue = random.randrange(colorA[2], colorB[2]+1)
    alpha = random.randrange(colorA[3], colorB[3]+1)
    return (red, green, blue, alpha)


class LeafBunch:
    def __init__(self, center, height, width, color=LEAF_COLOR):
        self.center = center
        self.height = height
        self.width = width
        self.color = LEAF_COLOR
    def __init__(self, center, diameter):
        self.center = center
        self.height = diameter
        self.width = diameter
    def draw(self, draw : ImageDraw.ImageDraw):
        x1 = self.center[0] - self.width/2
        y1 = self.center[1] - self.height/2
        x2 = self.center[0] + self.width/2
        y2 = self.center[1] + self.height/2
        points = (x1, y1, x2, y2)
        draw.ellipse(points, fill=self.color)




def drawBranch(startPoint, endPoint, width, resolution, draw : ImageDraw.ImageDraw):
    length = getDistance(startPoint, endPoint)
    points = int(length/resolution)
    for i in range(points+1):
        ratio = i/points
        center = interpolate(startPoint, endPoint, ratio)
        ellipsePoints = getBoundariesForCircle(center, width)
        draw.ellipse(ellipsePoints, fill=BRANCH_COLOR)
    return    






def drawPoint(center, diameter, draw : ImageDraw.ImageDraw, color=BRANCH_COLOR):
    x1 = center[0] - diameter/2
    y1 = center[1] - diameter/2
    x2 = center[0] + diameter/2
    y2 = center[1] + diameter/2
    points = (x1, y1, x2, y2)
    draw.ellipse(points, fill=color)


SPLIT_RATIO = 0.1
DECAY_RATIO = 0.99
ANGLE_DECAY_RATIO = 0.95
MIN_DIAMETER = 2
LEAF_BACK_DIAMETER = 60
LEAF_FORE_DIAMETER = 90
MAX_LEAF_Y = START[1]-90


def drawBranchRecursive(startPoint, diameter, angle, resolution, branchDraw : ImageDraw.ImageDraw, leafBackgroundDraw : ImageDraw.ImageDraw, leafForegroundDraw : ImageDraw.ImageDraw, branchColor=BRANCH_COLOR, leafColor=LEAF_COLOR):
    drawPoint(startPoint, diameter, branchDraw, color=branchColor)
    if random.random() < SPLIT_RATIO:
        # split
        splitRatio = random.random()
        diameterA = math.sqrt(splitRatio) * diameter
        diameterB = math.sqrt(1-splitRatio) * diameter
        relAngleA = randRangeFloat(0, radians(30))
        relAngleB = randRangeFloat(0, radians(-30))
        correctionAngle = math.asin( (math.sin(relAngleA)*diameterA + math.sin(relAngleB)*diameterB)/(diameterA + diameterB) )
        angleA = angle + relAngleA - correctionAngle
        angleB = angle + relAngleB - correctionAngle
        drawBranchRecursive(startPoint, diameterA, angleA, resolution, branchDraw, leafBackgroundDraw, leafForegroundDraw, branchColor)
        drawBranchRecursive(startPoint, diameterB, angleB, resolution, branchDraw, leafBackgroundDraw, leafForegroundDraw, branchColor)
    else:
        nextPointX = startPoint[0] + math.cos(angle) * resolution
        nextPointY = startPoint[1] + math.sin(angle) * resolution
        nextPoint = [nextPointX, nextPointY]
        nextDiameterRatio = randRangeFloat(DECAY_RATIO, 1)
        nextDiameter = nextDiameterRatio * diameter
        nextAngle = randRangeFloat(angle, interpolateScalar(radians(-90), angle, ANGLE_DECAY_RATIO))
        if nextDiameter >= MIN_DIAMETER:
            drawBranchRecursive(nextPoint, nextDiameter, nextAngle, resolution, branchDraw, leafBackgroundDraw, leafForegroundDraw, branchColor)
        else:
            if (startPoint[1] <= MAX_LEAF_Y):
                modifiedLeafColor = getRandomColorFromRange(LEAF_COLOR_MIN, LEAF_COLOR_MAX)
                drawPoint(startPoint, LEAF_BACK_DIAMETER, leafBackgroundDraw, modifiedLeafColor)
                drawPoint(startPoint, LEAF_FORE_DIAMETER, leafForegroundDraw, modifiedLeafColor)
            


    

numToDraw = 30

OUTPUT_PATH = "sprites/objects/trees/"

for i in range(numToDraw):
    branchImage = Image.new('RGBA', SIZE, (0, 0, 0, 0))
    branchDraw = ImageDraw.Draw(branchImage)
    leafBackgroundImage = Image.new('RGBA', SIZE, (0, 0, 0, 0))
    leafBackgroundDraw = ImageDraw.Draw(leafBackgroundImage)
    leafForegroundImage = Image.new('RGBA', SIZE, (0, 0, 0, 0))
    leafForegroundDraw = ImageDraw.Draw(leafForegroundImage)
    drawBranchRecursive(START, 20, radians(-90), 3, branchDraw, leafBackgroundDraw, leafForegroundDraw)
    treeImage = Image.new('RGBA', SIZE, (0, 0, 0, 0))
    treeImage = Image.alpha_composite(leafBackgroundImage, branchImage)
    treeImage = Image.alpha_composite(treeImage, leafForegroundImage)
    filename = OUTPUT_PATH + "deciduous_" + str(i) + ".png"
    treeImage.save(filename, "PNG")



