

from PIL import Image, ImageDraw
import math

import players


def degreesToRadians(degrees):
  return(degrees / 180 * math.pi)

class Location:
  def __init__(self):
    self.x = 0
    self.y = 0
    self.z = 0
  def __init__(self, coordinates):
    self.x = coordinates[0]
    self.y = coordinates[1]
    self.z = coordinates[2]
  def plus(self, location):
    x = self.x + location.x
    y = self.y + location.y
    z = self.z + location.z
    return Location((x, y, z))
  ## Add a length plus angle on the XZ plane
  def plusXZAngleLength(self, xzAngle, length):
    x = self.x + length * math.cos(xzAngle)
    y = self.y
    z = self.z + length * math.sin(xzAngle)
    return Location((x, y, z))
  def toString(self):
    output = "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"
    return output
    


class BodyAttributes:
  def __init__(self):
    ## Lengths
    self.torsoLength = 8
    self.femurLength = 7
    self.tibiaLength = 7
    self.footLength = 2.5
    self.humerusLength = 5
    self.radiusLength = 5
    self.hipWidth = 1.5
    self.shoulderWidth = 2
    self.headBottomHeight=3
    self.headTopHeight=4.7
    self.headBottomOffset=0.3
    self.headTopOffset=0.2
    ## Ratios
    self.shortsFemurRatio=0.5
    self.shortsTorsoRatio=0.2
    self.hairRadiusRatio=0.9
    ## Sizes
    self.hipRadius = 1.4
    self.kneeRadius = 1.0
    self.ankleRadius = 0.7
    self.toeRadius = 0.6
    self.shoulderTorsoRadius = 1.6
    self.shoulderRadius = 1
    self.elbowRadius=0.8
    self.wristRadius=0.5
    self.handRadius=1
    self.headTopRadius=1.6
    self.headBottomRadius=1.2
    self.hairTopRadius = 0.4
    self.hairMiddleRadius = 0.6
    self.hairBottomRadius = 0.7
    ## Colors
    self.skinTone=(255, 230, 200, 255)
    self.singletColor=(0, 160, 0, 255)
    self.shortsColor=(10, 10, 10, 255)
    self.shoeColor=(0, 255, 0, 255)
    self.hairColor=(170, 125, 100, 255)

class BodyPositions:
  def __init__(self):
    ## Angles
    self.rightElbowAngle = degreesToRadians(180)
    self.leftElbowAngle = degreesToRadians(180)
    self.rightShoulderAngle = degreesToRadians(0)
    self.leftShoulderAngle = degreesToRadians(0)
    self.rightKneeAngle = degreesToRadians(180)
    self.leftKneeAngle = degreesToRadians(180)
    self.rightHipAngle = degreesToRadians(180)
    self.leftHipAngle = degreesToRadians(180)
    self.rightAnkleAngle = degreesToRadians(90)
    self.leftAnkleAngle = degreesToRadians(90)
    self.torsoToGroundAngle = degreesToRadians(90)
    self.torsoToGroundHeight = 14
  def interpolateWith(self, bodyPositions, ratio):
    interpolatedBodyPositions = BodyPositions()
    interpolatedBodyPositions.leftElbowAngle = self.leftElbowAngle + (bodyPositions.leftElbowAngle - self.leftElbowAngle) * ratio
    interpolatedBodyPositions.rightElbowAngle = self.rightElbowAngle + (bodyPositions.rightElbowAngle - self.rightElbowAngle) * ratio
    interpolatedBodyPositions.leftShoulderAngle = self.leftShoulderAngle + (bodyPositions.leftShoulderAngle - self.leftShoulderAngle) * ratio
    interpolatedBodyPositions.rightShoulderAngle = self.rightShoulderAngle + (bodyPositions.rightShoulderAngle - self.rightShoulderAngle) * ratio
    interpolatedBodyPositions.leftKneeAngle = self.leftKneeAngle + (bodyPositions.leftKneeAngle - self.leftKneeAngle) * ratio
    interpolatedBodyPositions.rightKneeAngle = self.rightKneeAngle + (bodyPositions.rightKneeAngle - self.rightKneeAngle) * ratio
    interpolatedBodyPositions.leftHipAngle = self.leftHipAngle + (bodyPositions.leftHipAngle - self.leftHipAngle) * ratio
    interpolatedBodyPositions.rightHipAngle = self.rightHipAngle + (bodyPositions.rightHipAngle - self.rightHipAngle) * ratio
    interpolatedBodyPositions.leftAnkleAngle = self.leftAnkleAngle + (bodyPositions.leftAnkleAngle - self.leftAnkleAngle) * ratio
    interpolatedBodyPositions.rightAnkleAngle = self.rightAnkleAngle + (bodyPositions.rightAnkleAngle - self.rightAnkleAngle) * ratio
    interpolatedBodyPositions.torsoToGroundAngle = self.torsoToGroundAngle + (bodyPositions.torsoToGroundAngle - self.torsoToGroundAngle) * ratio
    interpolatedBodyPositions.torsoToGroundHeight = self.torsoToGroundHeight + (bodyPositions.torsoToGroundHeight - self.torsoToGroundHeight) * ratio
    return interpolatedBodyPositions
  def invert(self):
    invertedBodyPosition = BodyPositions()
    invertedBodyPosition.leftElbowAngle = self.rightElbowAngle
    invertedBodyPosition.leftShoulderAngle = self.rightShoulderAngle
    invertedBodyPosition.leftHipAngle = self.rightHipAngle
    invertedBodyPosition.leftKneeAngle = self.rightKneeAngle
    invertedBodyPosition.leftAnkleAngle = self.rightAnkleAngle
    invertedBodyPosition.rightElbowAngle = self.leftElbowAngle
    invertedBodyPosition.rightShoulderAngle = self.leftShoulderAngle
    invertedBodyPosition.rightHipAngle = self.leftHipAngle
    invertedBodyPosition.rightKneeAngle = self.leftKneeAngle
    invertedBodyPosition.rightAnkleAngle = self.leftAnkleAngle
    invertedBodyPosition.torsoToGroundAngle = self.torsoToGroundAngle
    invertedBodyPosition.torsoToGroundHeight = self.torsoToGroundHeight
    return invertedBodyPosition


class BodyCoordinates:
  def __init__(self, bodyAttributes, bodyPositions):
    ## Torso
    self.torsoBottom = Location((0, 0, bodyPositions.torsoToGroundHeight))
    self.torsoTop = self.torsoBottom.plusXZAngleLength(bodyPositions.torsoToGroundAngle, bodyAttributes.torsoLength)
    ## Upper leg
    self.leftHip = self.torsoBottom.plus(Location((0, bodyAttributes.hipWidth/2, 0)))
    self.rightHip = self.torsoBottom.plus(Location((0, -bodyAttributes.hipWidth/2, 0)))
    leftHipToGroundAngle = bodyPositions.torsoToGroundAngle + bodyPositions.leftHipAngle
    rightHipToGroundAngle = bodyPositions.torsoToGroundAngle + bodyPositions.rightHipAngle
    self.leftKnee = self.leftHip.plusXZAngleLength(leftHipToGroundAngle, bodyAttributes.femurLength)
    self.rightKnee = self.rightHip.plusXZAngleLength(rightHipToGroundAngle, bodyAttributes.femurLength)
    ## Lower leg
    leftKneeToGroundAngle = leftHipToGroundAngle + degreesToRadians(180) + bodyPositions.leftKneeAngle
    rightKneeToGroundAngle = rightHipToGroundAngle + degreesToRadians(180) + bodyPositions.rightKneeAngle
    self.leftAnkle = self.leftKnee.plusXZAngleLength(leftKneeToGroundAngle, bodyAttributes.tibiaLength)
    self.rightAnkle = self.rightKnee.plusXZAngleLength(rightKneeToGroundAngle, bodyAttributes.tibiaLength)
    ## Foot
    leftAnkleToGroundAngle = leftKneeToGroundAngle + degreesToRadians(180) - bodyPositions.leftAnkleAngle
    rightAnkleToGroundAngle = rightKneeToGroundAngle + degreesToRadians(180) - bodyPositions.rightAnkleAngle
    self.leftToe = self.leftAnkle.plusXZAngleLength(leftAnkleToGroundAngle, bodyAttributes.footLength)
    self.rightToe = self.rightAnkle.plusXZAngleLength(rightAnkleToGroundAngle, bodyAttributes.footLength)
    ## Upper arm
    self.leftShoulder = self.torsoTop.plus(Location((0, bodyAttributes.shoulderWidth/2, 0)))
    self.rightShoulder = self.torsoTop.plus(Location((0, -bodyAttributes.shoulderWidth/2, 0)))
    leftShoulderToGroundAngle = bodyPositions.torsoToGroundAngle + degreesToRadians(180) - bodyPositions.leftShoulderAngle
    rightShoulderToGroundAngle = bodyPositions.torsoToGroundAngle + degreesToRadians(180) - bodyPositions.rightShoulderAngle
    self.leftElbow = self.leftShoulder.plusXZAngleLength(leftShoulderToGroundAngle, bodyAttributes.humerusLength)
    self.rightElbow = self.rightShoulder.plusXZAngleLength(rightShoulderToGroundAngle, bodyAttributes.humerusLength)
    ## Lower arm
    leftElbowToGroundAngle = leftShoulderToGroundAngle + degreesToRadians(180) - bodyPositions.leftElbowAngle
    rightElbowToGroundAngle = rightShoulderToGroundAngle + degreesToRadians(180) - bodyPositions.rightElbowAngle
    self.leftHand = self.leftElbow.plusXZAngleLength(leftElbowToGroundAngle, bodyAttributes.radiusLength)
    self.rightHand = self.rightElbow.plusXZAngleLength(rightElbowToGroundAngle, bodyAttributes.radiusLength)
    ## Head
    headOffsetAngle = bodyPositions.torsoToGroundAngle - degreesToRadians(90)
    self.headTop = self.torsoTop.plusXZAngleLength(bodyPositions.torsoToGroundAngle, bodyAttributes.headTopHeight).plusXZAngleLength(headOffsetAngle, bodyAttributes.headBottomOffset)
    self.headBottom = self.torsoTop.plusXZAngleLength(bodyPositions.torsoToGroundAngle, bodyAttributes.headBottomHeight).plusXZAngleLength(headOffsetAngle, bodyAttributes.headTopOffset)
    self.hairTop = self.headTop.plusXZAngleLength(bodyPositions.torsoToGroundAngle - degreesToRadians(45), bodyAttributes.headTopRadius)
    self.hairMiddle = self.headTop.plusXZAngleLength(bodyPositions.torsoToGroundAngle + degreesToRadians(20), bodyAttributes.headTopRadius * bodyAttributes.hairRadiusRatio)
    self.hairBottom = self.headTop.plusXZAngleLength(bodyPositions.torsoToGroundAngle + degreesToRadians(105), bodyAttributes.headTopRadius * bodyAttributes.hairRadiusRatio * bodyAttributes.hairRadiusRatio)
  
  def toString(self):
    output = ""
    output += "torso bottom: " + self.torsoBottom.toString() + "\n"
    output += "torso top: " + self.torsoTop.toString() + "\n"
    output += "left hip: " + self.leftHip.toString() + "\n"
    output += "right hip: " + self.rightHip.toString() + "\n"
    output += "left knee: " + self.leftKnee.toString() + "\n"
    output += "right knee: " + self.rightKnee.toString() + "\n"
    output += "left ankle: " + self.leftAnkle.toString() + "\n"
    output += "right ankle: " + self.rightAnkle.toString() + "\n"
    output += "left toe: " + self.leftToe.toString() + "\n"
    output += "right toe: " + self.rightToe.toString() + "\n"
    output += "left shoulder: " + self.leftShoulder.toString() + "\n"
    output += "right shoulder: " + self.rightShoulder.toString() + "\n"
    output += "left elbow: " + self.leftElbow.toString() + "\n"
    output += "right elbow: " + self.rightElbow.toString() + "\n"
    output += "left hand: " + self.leftHand.toString() + "\n"
    output += "right hand: " + self.rightHand.toString() + "\n"
    output += "head bottom: " + self.headBottom.toString() + "\n"
    output += "head top: " + self.headTop.toString() + "\n"
    return output
    
    
    


class ViewAngle:
  def __init__(self, yzAngle, zoom, centerX, centerY):
    self.yRatio = math.sin(yzAngle)
    self.zRatio = math.cos(yzAngle)
    self.zoom = zoom
    self.centerX = centerX
    self.centerY = centerY
  def coordinateToScreen(self, location):
    x = self.centerX + self.zoom * location.x
    y = self.centerY - self.zoom * (self.yRatio * location.y + self.zRatio * location.z)
    return (x, y)
  def sizeToScreen(self, size):
    return (self.zoom * size)
    

class Circle:
  def __init__(self, coordinates, radius):
    self.coordinates = coordinates
    self.radius = radius
  def corners(self):
    return (self.coordinates[0]-self.radius, self.coordinates[1]-self.radius, self.coordinates[0]+self.radius, self.coordinates[1]+self.radius)
  def interpolateWith(self, circle, ratio):
    radius = self.radius + (circle.radius - self.radius) * ratio
    x = self.coordinates[0] + (circle.coordinates[0] - self.coordinates[0])*ratio
    y = self.coordinates[1] + (circle.coordinates[1] - self.coordinates[1])*ratio
    return Circle((x, y), radius)


RESOLUTION=10

def interpolateCircles(circleA, circleB, color, resolution, draw):
  draw.ellipse(circleA.corners(), fill=color)
  for i in range(1, resolution):
    circle = circleA.interpolateWith(circleB, i/resolution)
    draw.ellipse(circle.corners(), fill=color)
  draw.ellipse(circleB.corners(), fill=color)
    
def plotCircle(circle, color, draw):
  draw.ellipse(circle.corners(), fill=color)



def drawBody(bodyCoordinates, bodyAttributes, viewAngle, draw):
  ## Feet
  leftAnkleCoordinates = viewAngle.coordinateToScreen(bodyCoordinates.leftAnkle)
  rightAnkleCoordinates = viewAngle.coordinateToScreen(bodyCoordinates.rightAnkle)
  ankleRadius = viewAngle.sizeToScreen(bodyAttributes.ankleRadius)
  leftAnkleCircle = Circle(leftAnkleCoordinates, ankleRadius)
  rightAnkleCircle = Circle(rightAnkleCoordinates, ankleRadius)

  leftToeCoordinates = viewAngle.coordinateToScreen(bodyCoordinates.leftToe)
  rightToeCoordinates = viewAngle.coordinateToScreen(bodyCoordinates.rightToe)
  toeRadius = viewAngle.sizeToScreen(bodyAttributes.toeRadius)
  leftToeCircle = Circle(leftToeCoordinates, toeRadius)
  rightToeCircle = Circle(rightToeCoordinates, toeRadius)
  
  ## Lower legs
  leftKneeCoordinates = viewAngle.coordinateToScreen(bodyCoordinates.leftKnee)
  rightKneeCoordinates = viewAngle.coordinateToScreen(bodyCoordinates.rightKnee)
  kneeRadius = viewAngle.sizeToScreen(bodyAttributes.kneeRadius)
  leftKneeCircle = Circle(leftKneeCoordinates, kneeRadius)
  rightKneeCircle = Circle(rightKneeCoordinates, kneeRadius)
  
  
  ## Upper legs
  leftHipCoordinates = viewAngle.coordinateToScreen(bodyCoordinates.leftHip)
  rightHipCoordinates = viewAngle.coordinateToScreen(bodyCoordinates.rightHip)
  hipRadius = viewAngle.sizeToScreen(bodyAttributes.hipRadius)
  leftHipCircle = Circle(leftHipCoordinates, hipRadius)
  rightHipCircle = Circle(leftHipCoordinates, hipRadius)
  leftBottomShortsCircle = leftHipCircle.interpolateWith(leftKneeCircle, bodyAttributes.shortsFemurRatio)
  rightBottomShortsCircle = leftHipCircle.interpolateWith(rightKneeCircle, bodyAttributes.shortsFemurRatio)
  
  ## Torso
  leftShoulderCoordinates = viewAngle.coordinateToScreen(bodyCoordinates.leftShoulder)
  rightShoulderCoordinates = viewAngle.coordinateToScreen(bodyCoordinates.rightShoulder)
  shoulderTorsoRadius = viewAngle.sizeToScreen(bodyAttributes.shoulderTorsoRadius)
  leftShoulderTorsoCircle = Circle(leftShoulderCoordinates, shoulderTorsoRadius)
  rightShoulderTorsoCircle = Circle(rightShoulderCoordinates, shoulderTorsoRadius)
  leftShortsTopCircle = leftHipCircle.interpolateWith(leftShoulderTorsoCircle, bodyAttributes.shortsTorsoRatio)
  rightShortsTopCircle = rightHipCircle.interpolateWith(rightShoulderTorsoCircle, bodyAttributes.shortsTorsoRatio)
  
  ## Upper arm
  shoulderRadius = viewAngle.sizeToScreen(bodyAttributes.shoulderRadius)
  leftShoulderCircle = Circle(leftShoulderCoordinates, shoulderRadius)
  rightShoulderCircle = Circle(rightShoulderCoordinates, shoulderRadius)
  leftElbowCoordinates = viewAngle.coordinateToScreen(bodyCoordinates.leftElbow)
  rightElbowCoordinates = viewAngle.coordinateToScreen(bodyCoordinates.rightElbow)
  elbowRadius = viewAngle.sizeToScreen(bodyAttributes.elbowRadius)
  leftElbowCircle = Circle(leftElbowCoordinates, elbowRadius)
  rightElbowCircle = Circle(rightElbowCoordinates, elbowRadius)
  
  ## Lower arm
  leftHandCoordinates = viewAngle.coordinateToScreen(bodyCoordinates.leftHand)
  rightHandCoordinates = viewAngle.coordinateToScreen(bodyCoordinates.rightHand)
  handRadius = viewAngle.sizeToScreen(bodyAttributes.handRadius)
  wristRadius = viewAngle.sizeToScreen(bodyAttributes.wristRadius)
  leftHandCircle = Circle(leftHandCoordinates, handRadius)
  leftWristCircle = Circle(leftHandCoordinates, wristRadius)
  rightHandCircle = Circle(rightHandCoordinates, handRadius)
  rightWristCircle = Circle(rightHandCoordinates, wristRadius)
  
  ## Head
  headBottomCoordinates = viewAngle.coordinateToScreen(bodyCoordinates.headBottom)
  headTopCoordinates = viewAngle.coordinateToScreen(bodyCoordinates.headTop)
  headBottomRadius = viewAngle.sizeToScreen(bodyAttributes.headBottomRadius)
  headTopRadius = viewAngle.sizeToScreen(bodyAttributes.headTopRadius)
  headBottomCircle = Circle(headBottomCoordinates, headBottomRadius)
  headTopCircle = Circle(headTopCoordinates, headTopRadius)
  
  ## Hair
  hairTopCoordinates = viewAngle.coordinateToScreen(bodyCoordinates.hairTop)
  hairMiddleCoordinates = viewAngle.coordinateToScreen(bodyCoordinates.hairMiddle)
  hairBottomCoordinates = viewAngle.coordinateToScreen(bodyCoordinates.hairBottom)
  hairTopRadius = viewAngle.sizeToScreen(bodyAttributes.hairTopRadius)
  hairMiddleRadius = viewAngle.sizeToScreen(bodyAttributes.hairMiddleRadius)
  hairBottomRadius = viewAngle.sizeToScreen(bodyAttributes.hairBottomRadius)
  hairTopCircle = Circle(hairTopCoordinates, hairTopRadius)
  hairMiddleCircle = Circle(hairMiddleCoordinates, hairMiddleRadius)
  hairBottomCircle = Circle(hairBottomCoordinates, hairBottomRadius)
  
  
  
  
  
  ## Draw
  ### Left arm
  interpolateCircles(leftShoulderCircle, leftElbowCircle, bodyAttributes.skinTone, RESOLUTION, draw)
  interpolateCircles(leftElbowCircle, leftWristCircle, bodyAttributes.skinTone, RESOLUTION, draw)
  plotCircle(leftHandCircle, bodyAttributes.skinTone, draw)
  
  ### Left leg
  interpolateCircles(leftKneeCircle, leftAnkleCircle, bodyAttributes.skinTone, RESOLUTION, draw)
  interpolateCircles(leftKneeCircle, leftBottomShortsCircle, bodyAttributes.skinTone, RESOLUTION, draw)
  interpolateCircles(leftBottomShortsCircle, leftHipCircle, bodyAttributes.shortsColor, RESOLUTION, draw)
  interpolateCircles(leftAnkleCircle, leftToeCircle, bodyAttributes.shoeColor, RESOLUTION, draw)
  
  ### Right leg
  interpolateCircles(rightKneeCircle, rightAnkleCircle, bodyAttributes.skinTone, RESOLUTION, draw)
  interpolateCircles(rightAnkleCircle, rightToeCircle, bodyAttributes.shoeColor, RESOLUTION, draw)
  interpolateCircles(rightKneeCircle, rightBottomShortsCircle, bodyAttributes.skinTone, RESOLUTION, draw)
  interpolateCircles(rightBottomShortsCircle, rightHipCircle, bodyAttributes.shortsColor, RESOLUTION, draw)
  
  ### Torso
  interpolateCircles(leftHipCircle, leftShortsTopCircle, bodyAttributes.shortsColor, RESOLUTION, draw)
  interpolateCircles(rightHipCircle, rightShortsTopCircle, bodyAttributes.shortsColor, RESOLUTION, draw)
  interpolateCircles(leftShortsTopCircle, leftShoulderTorsoCircle, bodyAttributes.singletColor, RESOLUTION, draw)
  interpolateCircles(rightShortsTopCircle, rightShoulderTorsoCircle, bodyAttributes.singletColor, RESOLUTION, draw)
  
  ### Right arm
  interpolateCircles(rightShoulderCircle, rightElbowCircle, bodyAttributes.skinTone, RESOLUTION, draw)
  interpolateCircles(rightElbowCircle, rightWristCircle, bodyAttributes.skinTone, RESOLUTION, draw)
  plotCircle(rightHandCircle, bodyAttributes.skinTone, draw)
  
  ### Head
  interpolateCircles(headBottomCircle, headTopCircle, bodyAttributes.skinTone, RESOLUTION, draw)
  
  ### Hair
  if (bodyAttributes.hairColor[3] != 0):
    interpolateCircles(hairTopCircle, hairMiddleCircle, bodyAttributes.hairColor, RESOLUTION, draw)
    interpolateCircles(hairMiddleCircle, hairBottomCircle, bodyAttributes.hairColor, RESOLUTION, draw)
  
  
  ## Lower legs
  ## Upper legs
  ## Torso
  ## Upper arms
  ## Lower arms
  ## Head
  


myViewAngle = ViewAngle(degreesToRadians(30), 5, 75, 200)
myBodyAttributes = BodyAttributes()
myBodyPositions = BodyPositions()


DEFAULT_TORSO_TO_GROUND_ANGLE = degreesToRadians(85)
# right foot forward
rightForwardBodyPositions = BodyPositions()

rightForwardBodyPositions.torsoToGroundAngle = DEFAULT_TORSO_TO_GROUND_ANGLE
rightForwardBodyPositions.torsoToGroundHeight = 13.66
rightForwardBodyPositions.leftHipAngle = degreesToRadians(120)
rightForwardBodyPositions.leftKneeAngle = degreesToRadians(90)
rightForwardBodyPositions.rightHipAngle = degreesToRadians(260)
rightForwardBodyPositions.rightKneeAngle = degreesToRadians(135)
rightForwardBodyPositions.leftElbowAngle = degreesToRadians(50)
rightForwardBodyPositions.rightElbowAngle = degreesToRadians(120)
rightForwardBodyPositions.leftShoulderAngle = degreesToRadians(-30)
rightForwardBodyPositions.rightShoulderAngle = degreesToRadians(65)
rightForwardBodyPositions.leftAnkleAngle = degreesToRadians(110)
rightForwardBodyPositions.rightAnkleAngle = degreesToRadians(90)

# right foot max extent
rightPlantBodyPositions = BodyPositions()
rightPlantBodyPositions.torsoToGroundAngle = DEFAULT_TORSO_TO_GROUND_ANGLE
rightPlantBodyPositions.torsoToGroundHeight = 13.89
rightPlantBodyPositions.rightHipAngle = degreesToRadians(200)
rightPlantBodyPositions.rightKneeAngle = degreesToRadians(155)
rightPlantBodyPositions.rightAnkleAngle = degreesToRadians(70)
rightPlantBodyPositions.rightShoulderAngle = degreesToRadians(15)
rightPlantBodyPositions.rightElbowAngle = degreesToRadians(105)
rightPlantBodyPositions.leftHipAngle = degreesToRadians(180)
rightPlantBodyPositions.leftKneeAngle = degreesToRadians(80)
rightPlantBodyPositions.leftAnkleAngle = degreesToRadians(120)
rightPlantBodyPositions.leftShoulderAngle = degreesToRadians(-15)
rightPlantBodyPositions.leftElbowAngle = degreesToRadians(90)

# right toe-off
rightToeoffBodyPositions = BodyPositions()
rightToeoffBodyPositions.torsoToGroundAngle = DEFAULT_TORSO_TO_GROUND_ANGLE
rightToeoffBodyPositions.torsoToGroundHeight = 15.5
rightToeoffBodyPositions.rightHipAngle = degreesToRadians(175)
rightToeoffBodyPositions.rightKneeAngle = degreesToRadians(165)
rightToeoffBodyPositions.rightAnkleAngle = degreesToRadians(80)
rightToeoffBodyPositions.rightShoulderAngle = degreesToRadians(5)
rightToeoffBodyPositions.rightElbowAngle = degreesToRadians(85)
rightToeoffBodyPositions.leftHipAngle = degreesToRadians(245)
rightToeoffBodyPositions.leftKneeAngle = degreesToRadians(70)
rightToeoffBodyPositions.leftAnkleAngle = degreesToRadians(90)
rightToeoffBodyPositions.leftShoulderAngle = degreesToRadians(10)
rightToeoffBodyPositions.leftElbowAngle = degreesToRadians(110)

#rightPlantBodyPositions.leftHipAngle = degreesToRadians(


leftForwardBodyPositions = rightForwardBodyPositions.invert()
leftPlantBodyPositions = rightPlantBodyPositions.invert()
leftToeoffBodyPositions = rightToeoffBodyPositions.invert()



#rightForwardBodyCoordinates = BodyCoordinates(myBodyAttributes, rightForwardBodyPositions)
#rightPlantBodyCoordinates = BodyCoordinates(myBodyAttributes, rightPlantBodyPositions)
#rightToeoffBodyCoordinates = BodyCoordinates(myBodyAttributes, rightToeoffBodyPositions)







# left foot forward

#print(rightForwardBodyCoordinates.toString())




bodyPositionsSet = [rightForwardBodyPositions, rightPlantBodyPositions, rightToeoffBodyPositions, leftForwardBodyPositions, leftPlantBodyPositions, leftToeoffBodyPositions]
framesAfter = [10, 5, 10, 10, 5, 10]

FRAMES_PER_POSITION=10

#frameCount = 0

#frames = []


drawnCount = 0

lookCount = 0
for commonLook in players.commonLooks:
  kitCount = 0
  for professionalKit in players.professionalKits:
    thisBodyAttributes = BodyAttributes()
    thisBodyAttributes.singletColor = players.professionalKits[professionalKit].singletColor
    thisBodyAttributes.shortsColor = players.professionalKits[professionalKit].shortsColor
    thisBodyAttributes.shoeColor = players.professionalKits[professionalKit].shoeColor
    thisBodyAttributes.skinTone = commonLook.skinTone
    thisBodyAttributes.hairColor = commonLook.hairColor
    frameCount = 0
    for i in range(len(bodyPositionsSet)):
      numFrames = framesAfter[i]
      for j in range(numFrames):
        filename = "sprites/player/" + str(kitCount) + "_" + str(lookCount) + "_" + str(frameCount) + ".png"
        bodyPositionsStart = bodyPositionsSet[i]
        bodyPositionsEnd = bodyPositionsSet[(i+1) % len(bodyPositionsSet)]
        interpolateRatio = j/FRAMES_PER_POSITION
        bodyPositionsToPlot = bodyPositionsStart.interpolateWith(bodyPositionsEnd, interpolateRatio)
        bodyCoordinatesToPlot = BodyCoordinates(thisBodyAttributes, bodyPositionsToPlot)
        image = Image.new('RGBA', (150, 300), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        drawBody(bodyCoordinatesToPlot, thisBodyAttributes, myViewAngle, draw)
    #    frames.append(image)
        image.save(filename, "PNG")
        frameCount += 1
    kitCount += 1
    drawnCount += 1
  lookCount += 1
  print("Drawn: " + str(drawnCount))





#frames[0].save("sprites/test.gif", format="GIF", append_images=frames[1:], save_all=True, duration=100, loop=0)

#drawBody(rightForwardBodyCoordinates, myBodyAttributes, myViewAngle, draw)
#drawBody(rightPlantBodyCoordinates, myBodyAttributes, myViewAngle, draw)
#drawBody(rightToeoffBodyCoordinates, myBodyAttributes, myViewAngle, draw)

#image.show()



