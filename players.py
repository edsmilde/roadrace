


skinTones = {}
skinTones['light'] = (255, 230, 200, 255)
skinTones['medium light'] = (206, 165, 130, 255)
skinTones['medium'] = (133, 85, 60, 255)
skinTones['medium dark'] = (78, 40, 25, 255)
skinTones['dark'] = (60, 35, 15, 255)

hairColors = {}
hairColors['blonde'] = (240, 210, 180, 255)
hairColors['brown'] = (180, 160, 130, 255)
hairColors['dark'] = (120, 90, 80, 255)
hairColors['red'] = (240, 170, 140, 255)
hairColors['black'] = (40, 20, 15, 255)
hairColors['bald'] = (0, 0, 0, 0)


class Kit:
  def __init__(self, singletColor, shortsColor):
    self.singletColor=singletColor
    self.shortsColor=shortsColor

professionalKits = {}

professionalKits['otc'] = Kit((0, 160, 0, 255), (10, 10, 10, 255)) # OTC
professionalKits['btc'] = Kit((180, 0, 0, 255), (10, 10, 10, 255)) # BTC
professionalKits['nn'] = Kit((220, 220, 220, 255), (255, 140, 0, 255)) # NN
# Nike purple
# Nike orange
# Brooks
# Adidas blue
# NOP
# Nike blue green
# Nike blue orange
# Army camo
# Saucony blue
# Asics orange
# Skechers red blue

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


players.append(
  Player(
    Name('Abdi', 'Abdirahman'),
    BodyShapeModifications(0.7, 0, 0.9, 71),
    ColorModifications('medium dark', 'bald', 'nike blue green', 'vaporfly green'),
    'US'))

players.append(
  Player(
    Name('Eliud', 'Kipchoge'),
    BodyShapeModifications(0, 0, 0.9, 67),
    ColorModifications('medium dark', 'bald', 'nn', 'vaporfly green'),
    'KE'))

players.append(
  Player(
    Name('Kenenisa', 'Bekele'),
    BodyShapeModifications(0, 0, 1, 65),
    ColorModifications('medium', 'dark', 'nn', 'vaporfly green'),
    'ET'))






