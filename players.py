


skinTones = {}
skinTones['light'] = (255, 230, 200, 255)
skinTones['medium light'] = (206, 165, 130, 255)
skinTones['medium'] = (133, 85, 60, 255)
skinTones['medium dark'] = (78, 40, 25, 255)
skinTones['dark'] = (60, 35, 15, 255)

hairColors = {}
hairColors['blonde'] = (240, 200, 170, 255)
hairColors['brown'] = (170, 125, 100, 255)
hairColors['dark'] = (120, 80, 80, 255)
hairColors['red'] = (240, 170, 90, 255)
hairColors['black'] = (80, 45, 30, 255)
hairColors['bald'] = (0, 0, 0, 0)

class Look:
  def __init__(self, skinToneName, hairColorName):
    self.skinTone = skinTones[skinToneName]
    self.hairColor = hairColors[hairColorName]

commonLooks = []

commonLooks.append(Look('light', 'blonde'))
commonLooks.append(Look('light', 'brown'))
commonLooks.append(Look('light', 'dark'))
commonLooks.append(Look('light', 'red'))
commonLooks.append(Look('light', 'bald'))
commonLooks.append(Look('medium light', 'brown'))
commonLooks.append(Look('medium light', 'dark'))
commonLooks.append(Look('medium light', 'black'))
commonLooks.append(Look('medium light', 'bald'))
commonLooks.append(Look('medium', 'dark'))
commonLooks.append(Look('medium', 'black'))
commonLooks.append(Look('medium', 'bald'))
commonLooks.append(Look('medium dark', 'black'))
commonLooks.append(Look('medium dark', 'bald'))
commonLooks.append(Look('dark', 'black'))
commonLooks.append(Look('dark', 'bald'))





class Kit:
  def __init__(self, singletColor, shortsColor, shoeColor):
    self.singletColor=singletColor
    self.shortsColor=shortsColor
    self.shoeColor=shoeColor

professionalKits = {}

# OTC
professionalKits['otc'] = Kit((0, 160, 0, 255), (10, 10, 10, 255), (0, 255, 0, 255))
# BTC
professionalKits['btc'] = Kit((180, 0, 0, 255), (10, 10, 10, 255), (255, 130, 0, 255))
# NN
professionalKits['nn'] = Kit((220, 220, 220, 255), (255, 200, 150, 255), (0, 255, 0, 255))
# Nike purple green
professionalKits['nike purple green'] = Kit((0, 200, 0, 255), (170, 0, 120, 255), (255, 130, 0, 255))
# Nike purple orange
professionalKits['nike purple orange'] = Kit((180, 130, 0, 255), (170, 0, 120, 255), (0, 255, 0, 255))
# Brooks
professionalKits['brooks'] = Kit((120, 200, 255, 255), (10, 10, 10, 255), (0, 40, 90, 255))
# Saucony blue
professionalKits['saucony blue'] = Kit((140, 160, 255, 255), (10, 10, 10, 255), (240, 240, 240, 255))
# Adidas white
professionalKits['adidas white'] = Kit((240, 240, 240, 255), (140, 160, 255), (240, 240, 240, 255))
# NOP
professionalKits['nop'] = Kit((60, 60, 60, 255), (20, 20, 20, 255), (0, 255, 0, 255))
# WCAP
professionalKits['wcap'] = Kit((120, 200, 160, 255), (10, 10, 10, 255), (0, 255, 0, 255))
# Asics
professionalKits['asics'] = Kit((240, 130, 0, 255), (10, 10, 10, 255), (200, 200, 40, 255))
# Skechers
professionalKits['skechers'] = Kit((30, 70, 30, 255), (120, 200, 255, 255), (50, 50, 120, 255))
# Hoka
professionalKits['hoka'] = Kit((150, 180, 240), (140, 140, 180), (220, 240, 80))

internationalKits = {}
# Kenya
# USA
# Morocco
# Ethiopia
# Canada
# GB
# Norway
# Belgium
# Spain
# Netherlands
# Japan
# Italy
# France
# Switzerland
# NZ
# Australia

shoeColors = {}

shoeColors['vaporfly green'] = (0, 0, 255, 255)
shoeColors['vaporfly pink'] = (255, 130, 0, 255)
shoeColors['neutral white'] = (220, 220, 220, 255)
shoeColors['neutral black'] = (10, 10, 10, 255)
shoeColors['neutral gray'] = (120, 120, 120, 255)

countries = {}

class Skills:
  def __init__(self, energy, impatience, kick, consistency):
    self.energy = energy
    self.impatience = impatience
    self.kick = kick
    self.consistency = consistency
    

class BodyShapeModifications:
  def __init__(self, skull, shoulders, thinness, heightInches):
    self.skull = skull
    self.shoulders = shoulders
    self.thinness = thinness
    self.height = heightInches

class ColorModifications:
  def __init__(self, skinTone, hairColor, professionalKitName, shoeColorName):
    self.skinTone = skinTone
    self.hairColor = hairColor
    self.shortsColor = professionalKits[professionalKitName].shortsColor
    self.singletColor = professionalKits[professionalKitName].singletColor
    self.shoeColor = shoeColors[shoeColorName]
    
class Name:
  def __init__(self, firstName, lastName):
    self.firstName = firstName
    self.lastName = lastName


class Player:
  def __init__(self, name, bodyShapeModifications, colorModifications, countryCode):
    self.name = name
    self.bodyShapeModifications = bodyShapeModifications
    self.colorModifications = colorModifications
    self.countryCode = countryCode
    self.internationalKit = internationalKits[countryCode]
    


players = []








