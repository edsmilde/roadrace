import csv
import re

from players import professionalKits, commonLooks

CSV_FILENAME = "./players/players.csv"
OUTPUT_JS_FILENAME = "./js/data/players_data.js"


# Open files
#

csvFile = open(CSV_FILENAME, mode='r', encoding='utf-8-sig')
outputJsFile = open(OUTPUT_JS_FILENAME, 'w')
playerDataReader = csv.DictReader(csvFile)


def toVarName(name):
    varName = "player_" + re.sub("[^A-Za-z]", "", name)
    return varName

def newlines(n : int) -> str:
    newlinesString = ""
    for i in range(n):
        newlinesString += "\n"
    return newlinesString



def getSprite(hairColor, skinTone, kit):
    # find kit
    kitSprite = 0
    if not kit:
        kitSprite = 0
    else:
        for kitKey in professionalKits:
            if kit == kitKey:
                break
            kitSprite += 1
    lookSprite = 0
    # find look
    for look in commonLooks:
        if look.skinToneName == skinTone and look.hairColorName == hairColor:
            break
        lookSprite += 1
    return str(kitSprite) + "_" + str(lookSprite)
    


# Write player data
#

outputJsFile.write("var playerInfo = []")
outputJsFile.write(newlines(2))



playerFieldNames = []
playerFieldsRequired = {}
playerFieldsOptional = {}

playerId = 0

JS_PLAYER_FORMAT = "playerInfo[{playerId}] = new PlayerInfo('{name}', '{nation}', '{sprite}', {startEnergy}, {impatienceFactor});"

for playerData in playerDataReader:
    if len(playerFieldNames) == 0:
        for key in playerData:
            if key.startswith("Field"):
                playerFieldNames.append(key)
                playerFieldsRequired[key] = []
                playerFieldsOptional[key] = []
    name = playerData["FirstName"]
    nation = playerData["CountryCode"]
    kit = playerData["ProfessionalKit"]
    skinTone = playerData["SkinTone"]
    hairColor = playerData["HairColor"]
    sprite = getSprite(hairColor, skinTone, kit)
    # Todo: select correct sprite
    startEnergy = playerData["StartEnergy"]
    impatienceFactor = playerData["ImpatienceFactor"]
    jsLine = JS_PLAYER_FORMAT.format(playerId=playerId, name=name, nation=nation, sprite=sprite, startEnergy=startEnergy, impatienceFactor=impatienceFactor)
    outputJsFile.write(jsLine)
    outputJsFile.write(newlines(1))
    # Get competitive fields
    if len(playerFieldNames) == 0:
        for key in playerData:
            if key.startswith("Field"):
                playerFieldNames.append(key)
                playerFieldsRequired[key] = []
                playerFieldsOptional[key] = []
    for field in playerFieldNames:
        if playerData[field] == "optional":
            playerFieldsOptional[field].append(playerId)
        elif playerData[field] == "required":
            playerFieldsRequired[field].append(playerId)
    playerId += 1
    
outputJsFile.write(newlines(2))

# Write field data
#

outputJsFile.write("var fieldsOptional = {};" + newlines(1))
outputJsFile.write("var fieldsRequired = {};" + newlines(2))



JS_FIELD_FORMAT = "{arrayName}['{fieldName}'] = {fieldList};"

for fieldName in playerFieldNames:
    fieldListOptional = str(playerFieldsOptional[fieldName])
    fieldListRequired = str(playerFieldsRequired[fieldName])
    optionalFieldLine = JS_FIELD_FORMAT.format(arrayName="fieldsOptional", fieldName=fieldName, fieldList=fieldListOptional)
    requiredFieldLine = JS_FIELD_FORMAT.format(arrayName="fieldsRequired", fieldName=fieldName, fieldList=fieldListRequired)
    outputJsFile.write(optionalFieldLine + newlines(1))
    outputJsFile.write(requiredFieldLine + newlines(2))



csvFile.close()
outputJsFile.close()