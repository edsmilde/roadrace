
from PIL import Image, ImageDraw
import math
import random


SIZE=(500, 500)

START=(250, 400)



def height(size):
  return size[1]

def width(size):
  return size[0]

def radians(degrees):
  return degrees/180*math.pi

def drawBranch(startPoint, width, length, angle, draw):
  endPoint = (
    startPoint[0] + length*math.cos(angle),
    startPoint[1] - length*math.sin(angle)
  )
  draw.line((startPoint, endPoint), width=int(width), fill=(0, 0, 0, 255))
  return endPoint


def drawBranchRecursive(startPoint, width, length, angle, draw, minWidth):
  if width <= minWidth:
    return
  nextPoint = drawBranch(startPoint, width, length, angle, draw)
  
  randomA = 0.5+random.random()
  randomB = 0.5+random.random()
  randomC = 0.5+random.random()
  
  ratioTotal = math.sqrt(randomA*randomA + randomB*randomB + randomC*randomC)
  ratioA = randomA/ratioTotal
  ratioB = randomB/ratioTotal
  ratioC = randomC/ratioTotal
  
  angleA = radians(45+random.random()*90)
  angleB = radians(45+random.random()*90)
  angleC = radians(45+random.random()*90)
  
  widthA = width*ratioA
  widthB = width*ratioB
  widthC = width*ratioC
  
  lengthA = length*ratioA
  lengthB = length*ratioB
  lengthC = length*ratioC
  
  drawBranchRecursive(nextPoint, widthA, lengthA, angleA, draw, minWidth)
  drawBranchRecursive(nextPoint, widthB, lengthB, angleB, draw, minWidth)
  drawBranchRecursive(nextPoint, widthC, lengthC, angleC, draw, minWidth)
  




myImage = Image.new('RGBA', SIZE, (0, 0, 0, 0))

myDraw = ImageDraw.Draw(myImage)

drawBranchRecursive((150, 400), 10, 50, radians(90), myDraw, 2)
drawBranchRecursive((200, 400), 10, 50, radians(90), myDraw, 2)
drawBranchRecursive((250, 400), 10, 50, radians(90), myDraw, 2)
drawBranchRecursive((300, 400), 10, 50, radians(90), myDraw, 2)
drawBranchRecursive((350, 400), 10, 50, radians(90), myDraw, 2)


myImage.show()



