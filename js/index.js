

var userState = {
    started: false,
    playerInfo: {
        appearance: 0,
        kit: 0,
        name: ""
    },
    bestFinish: [],
    points: 0,
    badges: {},
};


var COOKIE_NAME = "hobbyjoggerhero_state";
var COOKIE_EXPIRE_DAYS = 365;



function saveUserState() {
  var userStateText = JSON.stringify(userState);
  Cookies.set(COOKIE_NAME, userStateText, {expires: COOKIE_EXPIRE_DAYS})
}

function loadUserState() {
  var userStateText = Cookies.get(COOKIE_NAME);
  
  if (userStateText) {
    userState = JSON.parse(userStateText);
  }
  
}

function loadGame() {
  loadUserState();
  populateRaceMenu();
  if (!userState.started) {
    loadCreatePlayer();
  } else {
    loadRaceMenu();
  }
}


// Race Menu

function nameToId(raceName) {
  var nameWithoutSpace = raceName.replace(/ /g, "");
  var id = nameWithoutSpace.toLowerCase();
  return id;
}

function getRaceButtonLink(race) {
  var raceButtonLink = document.createElement("a");
  raceButtonLink.setAttribute("href", "javascript:selectRace('" + nameToId(race.raceName) + "')");
  raceButtonLink.setAttribute("class", "raceButtonLink");
  var raceButtonDiv = document.createElement("div");
  raceButtonDiv.setAttribute("id", nameToId(race.raceName));
  raceButtonDiv.setAttribute("class", "raceButton");
  raceButtonDiv.innerHTML = race.raceName;
  raceButtonLink.appendChild(raceButtonDiv);
  return raceButtonLink;
}

function getRaceTierDiv(raceTier) {
  var raceTierDiv = document.createElement("div");
  raceTierDiv.setAttribute("class", "raceTier");
  var raceTierNameDiv = document.createElement("div");
  raceTierNameDiv.setAttribute("class", "raceTierName");
  raceTierNameDiv.innerHTML = raceTier.raceTierName;
  raceTierDiv.appendChild(raceTierNameDiv);
  for (var i = 0; i < raceTier.races.length; i++) {
    var raceButtonDiv = getRaceButtonLink(raceTier.races[i]);
    raceTierDiv.appendChild(raceButtonDiv);
  }
  return raceTierDiv;
}

function populateRaceMenu() {
  var raceMenuDiv = document.getElementById("raceMenu");
  for (var i = 0; i < raceTiers.length; i++) {
    var raceTierDiv = getRaceTierDiv(raceTiers[i]);
    raceMenuDiv.appendChild(raceTierDiv);
    
  }
}


function loadRaceMenu() {
  var raceMenuDiv = document.getElementById("raceMenu");
  raceMenuDiv.style.display = "block";
}


function selectRace(raceName) {
  // Find race name by id
  var selectedRace;
  for (var i = 0; i < raceTiers.length; i++) {
    for (var j = 0; j < raceTiers[i].races.length; j++) {
      if (raceName == nameToId(raceTiers[i].races[j].raceName)) {
        selectedRace = raceTiers[i].races[j];
        break;
      }
    }
  }
}

// Create player

var spritePrefix = "sprites/player/";
var spriteSuffix = "_0.png";

var numKits = 13;
var numAppearances = 16;

var selectedKit = 0;
var selectedAppearance = 0;

var BORDER_STYLE_SELECTED = "solid 1px black";

function loadCreatePlayer() {
    
    for (var i = 0; i < numAppearances; i++) {
        var appearanceImagePath = spritePrefix + selectedKit + "_" + i + spriteSuffix;
        var appearanceImage = document.createElement("img");
        appearanceImage.setAttribute("src", appearanceImagePath);
        appearanceImage.setAttribute("class", "playerSpriteImage");
        appearanceImage.setAttribute("id", "playerAppearanceImage_" + i);
        var appearanceLink = document.createElement("a");
        appearanceLink.setAttribute("class", "playerSpriteLink");
        appearanceLink.setAttribute("href", "javascript:createPlayerSelectAppearance(" + i + ");");
        appearanceLink.appendChild(appearanceImage);
        var appearanceDiv = document.createElement("div");
        appearanceDiv.appendChild(appearanceLink);
        appearanceDiv.setAttribute("class", "playerSprite");
        appearanceDiv.setAttribute("id", "playerSpriteAppearance_" + i);
        document.getElementById("playerAppearances").appendChild(appearanceDiv);
    }
    
    for (var i = 0; i < numKits; i++) {
        var kitImagePath = spritePrefix + i + "_" + selectedAppearance + spriteSuffix;
        var kitImage = document.createElement("img");
        kitImage.setAttribute("src", kitImagePath);
        kitImage.setAttribute("class", "playerSpriteImage");
        kitImage.setAttribute("id", "playerKitImage_" + i);
        var kitLink = document.createElement("a");
        kitLink.appendChild(kitImage);
        kitLink.setAttribute("class", "playerSpriteLink");
        kitLink.setAttribute("href", "javascript:createPlayerSelectKit(" + i + ");");
        var kitDiv = document.createElement("div");
        kitDiv.appendChild(kitLink);
        kitDiv.setAttribute("class", "playerSprite");
        kitDiv.setAttribute("id", "playerSpriteKit_" + i);
        document.getElementById("playerKits").appendChild(kitDiv);
    }
    
    document.getElementById("playerSpriteKit_" + selectedKit).style.border = BORDER_STYLE_SELECTED;
    document.getElementById("playerSpriteAppearance_" + selectedAppearance).style.border = BORDER_STYLE_SELECTED;
    
    document.getElementById("createPlayer").style.display = "block";
    document.playerInfoForm.playerName.focus();
}

function createPlayerSelectKit(index) {
    selectedKit = index;
    for (var i = 0; i < numKits; i++) {
      var thisElement = document.getElementById("playerSpriteKit_" + i);
      if (i == index) {
        thisElement.style.border = BORDER_STYLE_SELECTED;
      } else {
        thisElement.style.border = "none";
      }
    }
    for (var i = 0; i < numAppearances; i++) {
        var appearanceImagePath = spritePrefix + selectedKit + "_" + i + spriteSuffix;
        var appearanceImageId = "playerAppearanceImage_" + i;
        document.getElementById(appearanceImageId).setAttribute("src", appearanceImagePath);
    }
}

function createPlayerSelectAppearance(index) {
    selectedAppearance = index;
    for (var i = 0; i < numAppearances; i++) {
      var thisElement = document.getElementById("playerSpriteAppearance_" + i);
      if (i == index) {
        thisElement.style.border = BORDER_STYLE_SELECTED;
      } else {
        thisElement.style.border = "none";
      }
    }
    for (var i = 0; i < numKits; i++) {
        var kitImagePath = spritePrefix + i + "_" + selectedAppearance + spriteSuffix;
        var kitImageId = "playerKitImage_" + i;
        document.getElementById(kitImageId).setAttribute("src", kitImagePath);
    }
}

function createPlayerSubmit() {
  userState.playerInfo.name = document.playerInfoForm.playerName.value;
  if (!userState.playerInfo.name) {
    document.playerInfoForm.playerName.focus();
    return;
  }
  userState.playerInfo.kit = selectedKit;
  userState.playerInfo.appearance = selectedAppearance;
  userState.started = true;
  saveUserState();
  closeCreatePlayer();
  loadRaceMenu();
}

function closeCreatePlayer() {
  document.getElementById("createPlayer").style.display = "none";
  document.getElementById("raceMenu").style.display = "block";
  
}



