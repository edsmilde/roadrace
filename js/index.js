

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

var MENU_SCREEN = 0;
var RACE_NOT_STARTED = 1;
var RACE_IN_PROGRESS = 2;
var RACE_FINISHED = 3;

var FINISH_SLOWDOWN_STEPS = 40;
var PLAYER_SPRITE_OFFSET = {x: 40, y: 95};
var PLAYER_SPRITE_SIZE = {width: 80, height: 160};

var FRAMES_PER_STRIDE = 50;


var gameState = {
  raceInfo: null,
  raceCompetitorsInfo: null,
  racePlayers: null,
  raceStatus: MENU_SCREEN,
  gameWindow: null,
  userPlayerIndex: 0,
  currentStep: 0
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



var ROAD_WIDTH = 200;

var globalViewAttributes = {
    gameCenter: {
      x: 0,
      y: 0
    },
    screenCenter: {
      x: 300,
      y: 250
    },
    scale: {
      x: 4,
      y: 2
    },
    screenDimensions: {
      width: 600,
      height: 500
    },
    zIndexOffset: 2000
}






function pointToScreen(point) {
    var dx = point.x - globalViewAttributes.gameCenter.x;
    var dy = point.y - globalViewAttributes.gameCenter.y;
    var screenX = globalViewAttributes.screenCenter.x + globalViewAttributes.scale.x*dx;
    var screenY = globalViewAttributes.screenCenter.y + globalViewAttributes.scale.y*dy;
    return new Point(screenX, screenY);
};
  
  
function screenPositionVisible(topLeftScreen, width, height) {
    var bottomRightScreen = new Point(topLeftScreen.x + width, topLeftScreen.y + height);
    if (topLeftScreen.x < globalViewAttributes.screenDimensions.width
      && bottomRightScreen.x > 0
      && topLeftScreen.y < globalViewAttributes.screenDimensions.height
      && bottomRightScreen.y > 0) {
      return true;
    }
    return false;
}
  
function pointVisibleOnScreen(topLeft, width, height) {
    var topLeftScreen = pointToScreen(topLeft);
    var bottomRight = new Point(topLeft.x + width, topLeft.y + height);
    var bottomRightScreen = pointToScreen(bottomRight);
    if (topLeftScreen.x < globalViewAttributes.screenDimensions.width
      && bottomRightScreen.x > 0
      && topLeftScreen.y < globalViewAttributes.screenDimensions.height
      && bottomRightScreen.y > 0) {
      return true;
    }
    return false;
}
  
function widthToScreen(width) {
    return width * globalViewAttributes.scale.x;
}
  
function heightToScreen(height) {
    return height * globalViewAttributes.scale.y;
}
  
function Player(position, contactDirection, nextMove, energy, spriteBase, strideTime, screenElement, playerId, impatienceFactor, name) {
    this.position = position;
    this.contactDirection = contactDirection;
    this.nextMove = nextMove;
    this.energy = energy;
    this.spriteBase = spriteBase;
    this.strideTime = strideTime;
    this.stridePhase = 0;
    this.name = name;
    this.element = document.createElement("img");
    this.element.setAttribute("src", spriteBase + "25.png");
    this.element.setAttribute("id", "player-" + playerId);
    var screenPosition = pointToScreen(this.position);
    this.element.style.left = screenPosition.x - PLAYER_SPRITE_OFFSET.x;
    this.element.style.top = screenPosition.y - PLAYER_SPRITE_OFFSET.y;
    this.element.style.width = PLAYER_SPRITE_SIZE.width;
    this.element.style.height = PLAYER_SPRITE_SIZE.height;
    this.element.style.zIndex = Math.floor(this.position.y) + globalViewAttributes.zIndexOffset;
    this.element.style.position = "absolute";
    this.impatienceFactor = impatienceFactor;
    screenElement.appendChild(this.element);
    this.finished = false;
    this.finishStep = 0;
    this.rank = 0;
    this._log = "";
    this.incrementStride = function(time, cadence) {
        this.stridePhase = (this.stridePhase + time*cadence) % this.strideTime;
    }
    this.render = function(screenElement) {
        var screenPosition = pointToScreen(this.position);
        this.element.style.left = screenPosition.x - PLAYER_SPRITE_OFFSET.x;
        this.element.style.top = screenPosition.y - PLAYER_SPRITE_OFFSET.y;
        this.element.style.zIndex = Math.floor(this.position.y) + globalViewAttributes.zIndexOffset;
    }
    this.refreshSprite = function() {
        var relativeStridePhase = this.stridePhase / this.strideTime;
        var frame = Math.floor(relativeStridePhase * FRAMES_PER_STRIDE);
        var sprite = spriteBase + frame + ".png";
        this.element.setAttribute("src", sprite);
    }
}

function Point(x, y) {
    this.x = x;
    this.y = y;
    this.toString = function() { return("(" + this.x + "," + this.y + ")"); };
}


function Move(speed, direction, intent) {
    this.speed = speed;
    this.direction = direction;
    this.intent = intent;
}

var SPEED_BASE = 0;
var SPEED_SURGE = 1;
var SPEED_SLOW = 2;
var SPEED_FINISHED = 3;
var DIRECTION_STRAIGHT = 0;
var DIRECTION_LEFT = 1;
var DIRECTION_RIGHT = 2;
var INTENT_DRAFT = 0;
var INTENT_SURGE = 1;
var INTENT_FINISHED=2;

var FINISH_SLOWDOWN_STEPS = 40;

var BASE_START_ENERGY = 400;
var BASE_IMPATIENCE_FACTOR = 10;


var SIM_STEP_TIME_MS = 25;
var BASE_VELOCITY = 2;
var SURGE_RATIO = 1.4;
var STEER_RATIO = 0.6;
var STEER_SLOWDOWN_RATIO = Math.sqrt(1 - STEER_RATIO*STEER_RATIO);
var FINISH_DISTANCE=5000;

var PLAYER_RADIUS=4;
//var PLAYER_RADIUS=3;

var DRAFT_LENGTH=12;
var DRAFT_WIDTH=12;
var DRAFT_ENERGY_RATIO=0.5;
var SLOW_ENERGY_GAIN=0.8;

var MIN_TARGET_DISTANCE=2;
var MIN_SURGE_AVOID_DISTANCE=0;
var SURGE_AVERAGE_LENGTH=80;

var KICK_DECISION_RATIO=0.8;
var IMPATIENCE_FACTOR=5;
var DRAFT_DECISION_LENGTH=7;

var MAX_KICK_BOOST = 1.2;

function MoveOption(move, potential) {
  this.move = move;
  this.potential = potential;
}



function ScreenPosition(left, top) {
  this.top = top;
  this.left = left;
}



function hideElement(id) {
  var element = document.getElementById(id);
  element.style.display = "none";
}

function showElement(id) {
  var element = document.getElementById(id);
  element.style.display = "block";
}

function showElementInline(id) {
  var element = document.getElementById(id);
  element.style.display = "inline-block";
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
  loadRace(selectedRace);
}

function getRandomSubset(set, n) {
  if (n >= set.length) {
    return set;
  }
  var selected = [];
  for (var i = 0; i < n; i++) {
    var selectIndex = Math.floor(Math.random()*set.length);
    selected.push(set[selectIndex]);
    set.splice(selectIndex, 1);
  }
  return selected;
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

// Gameplay
//

var gameWindow;

function loadRace(raceInfo) {
  // Get race data
  var numCompetitors = raceInfo.numCompetitors;
  var competitors = raceInfo.requiredCompetitors.slice();  

  var remainingNeeded = numCompetitors - competitors.length;
  if (remainingNeeded > 0) {
    var optionalPool = raceInfo.optionalCompetitors.slice();
    var optionalSelected = getRandomSubset(optionalPool, remainingNeeded);
    competitors = competitors.concat(optionalSelected)
  }
  gameState.raceInfo = raceInfo;
  gameState.raceCompetitorsInfo = competitors.slice();
  gameState.raceStatus = RACE_NOT_STARTED;
  gameState.currentStep = 0;

  var startButton = document.getElementById("startButton");
  startButton.style.zIndex = globalViewAttributes.zIndexOffset;
  startButton.style.display = "inline-block";

  gameState.gameWindow = document.getElementById("game");

  renderSelectedBackground(raceInfo.background, gameState.gameWindow);
  document.getElementById("raceMenu").style.display = "none";
  document.getElementById("game").style.display = "block";
}

function renderPlayers() {
  for (var i = 0; i < gameState.racePlayers.length; i++) {
    gameState.racePlayers[i].render(gameState.gameWindow);
  }

}

var PLAYER_SPRITE_DIR = "sprites/player/";
function initPlayers() {
  var numPlayers = gameState.raceCompetitorsInfo.length + 1;
  var userSlot = Math.floor(numPlayers/2);
  gameState.userPlayerIndex = userSlot;
  gameState.racePlayers = new Array();
  for (var i = 0; i < numPlayers; i++) {
    var x = 0;
    var y = ((i + 0.5)/numPlayers) * ROAD_WIDTH - ROAD_WIDTH/2;
    var position = new Point(x, y);
    var contactDirection = new Point(0, 0);
    var move = new Move(SPEED_BASE, DIRECTION_STRAIGHT, INTENT_DRAFT);
    var spriteBase;
    var strideTime;
    var impatienceFactor;
    var startEnergy;
    var name;
    // Check which player
    if (i != userSlot) {
      var thisPlayer = i;
      if (i > userSlot) {
        thisPlayer = thisPlayer - 1;
      }
      var thisPlayerIndex = gameState.raceCompetitorsInfo[thisPlayer];
      var thisPlayerInfo = playerInfo[thisPlayerIndex];
      spriteBase = PLAYER_SPRITE_DIR + thisPlayerInfo.sprite + "_";
      impatienceFactor = BASE_IMPATIENCE_FACTOR * thisPlayerInfo.impatienceFactor;
      startEnergy = BASE_START_ENERGY * thisPlayerInfo.startEnergy;
      strideTime = 500 + Math.floor(100*Math.random());
      name = thisPlayerInfo.name;
    } else {
      spriteBase = PLAYER_SPRITE_DIR + userState.playerInfo.kit + "_" + userState.playerInfo.appearance + "_";
      impatienceFactor = 1;
      startEnergy = BASE_START_ENERGY;
      strideTime = 500;
      name = userState.playerInfo.name;
    }
    var player = new Player(position, contactDirection, move, startEnergy, spriteBase, strideTime, gameState.gameWindow, i, impatienceFactor, name);
    gameState.racePlayers[i] = player;
  }

}

function startRace() {
  if (gameState.raceStatus == RACE_NOT_STARTED) {
    initPlayers();
    renderPlayers();
    document.getElementById("startButton").style.display = "none";
    gameState.raceStatus = RACE_IN_PROGRESS;
    doStepAndShow(0);
    refreshSprites();

  }
}


var playerKeyStates = {
  up: false,
  down: false,
  left: false,
  right: false
}
function handleKeyDown(event) {
  switch(event.keyCode) {
    case 37:
      // left
      playerKeyStates.left = true;
      break;
    case 38:
      // up
      playerKeyStates.up = true;
      break;
      
    case 39:
      // right
      playerKeyStates.right = true;
      break;
      
    case 40:
      playerKeyStates.down = true;
      // down
      break;
      
  }
}

function handleKeyUp(event) {
  switch(event.keyCode) {
    case 37:
      // left
      playerKeyStates.left = false;
      break;
    case 38:
      // up
      playerKeyStates.up = false;
      break;
      
    case 39:
      // right
      playerKeyStates.right = false;
      break;
      
    case 40:
      playerKeyStates.down = false;
      // down
      break;
  }
}




function doStepAndShow(numFinished) {
  var startTime = new Date();
  var newNumFinished = simulateStep(numFinished);
  //testDisplay();
  animate();
  var endTime = new Date();
  var durationMs = endTime.getTime() - startTime.getTime();
  var waitTime = SIM_STEP_TIME_MS - durationMs;
  if (waitTime < 0) { waitTime = 0; }

  gameState.currentStep++;
  var numPlayers = gameState.racePlayers.length;
  if (newNumFinished < numPlayers) {
    setTimeout('doStepAndShow(' + newNumFinished + ')', waitTime);
  }
}



function simulateStep(numFinished) {
  // Get next moves
  //
  var players = gameState.racePlayers;
  var numPlayers = players.length;
  for (var i = 0; i < numPlayers; i++) {
    players[i]._log = "";
    if (players[i].finished) {
      players[i].nextMove = new Move(SPEED_FINISHED, DIRECTION_STRAIGHT, INTENT_FINISHED);
      continue;
    }
    
    if (i == gameState.userPlayerIndex) {
      // Check direction
      if (playerKeyStates.up && !playerKeyStates.down) {
        players[i].nextMove.direction = DIRECTION_RIGHT;
      } else if (playerKeyStates.down && !playerKeyStates.up) {
        players[i].nextMove.direction = DIRECTION_LEFT;
      } else {
        players[i].nextMove.direction = DIRECTION_STRAIGHT;
      }
      
      // Check speed
      if (playerKeyStates.right && !playerKeyStates.left) {
        if (players[i].energy >= 1) {
          players[i].nextMove.intent = INTENT_SURGE;
          players[i].nextMove.speed = SPEED_SURGE;
        } else {
          players[i].nextMove.intent = INTENT_DRAFT;
          players[i].nextMove.speed = SPEED_BASE;
        }
      } else if (playerKeyStates.left && !playerKeyStates.right) {
          players[i].nextMove.intent = INTENT_DRAFT;
          players[i].nextMove.speed = SPEED_SLOW;
      } else {
          players[i].nextMove.intent = INTENT_DRAFT;
          players[i].nextMove.speed = SPEED_BASE;
      }
      
      continue;
    }
    
    
    if (players[i].energy >= 1) {
      var willSurge = false;
      
      // If surging, likely continue
      //
      
      if (players[i].nextMove.intent == INTENT_SURGE) {
        if (Math.random() > 1/SURGE_AVERAGE_LENGTH) {
          willSurge = true;
        }
      }
      
        
      
      // If not surging, possibly start
      //
      if (!willSurge) {
        var distanceToFinish = FINISH_DISTANCE - players[i].position.x;
        var energyToFinish = distanceToFinish / BASE_VELOCITY / SURGE_RATIO;
//        var surgeChance = IMPATIENCE_FACTOR / SURGE_AVERAGE_LENGTH * (players[i].energy*players[i].energy) / (energyToFinish*energyToFinish);
        var surgeChance = players[i].impatienceFactor / SURGE_AVERAGE_LENGTH * (players[i].energy*players[i].energy) / (energyToFinish*energyToFinish);
        if (Math.random() < surgeChance) {
          willSurge = true;
        }
        // If nearing the end, kick
        var kickChance = KICK_DECISION_RATIO * (players[i].energy*players[i].energy) / (energyToFinish*energyToFinish);
        if (Math.random() < surgeChance) {
          willSurge = true;
        }
      }
      // If surging, determine direction
      //
      if (willSurge) {
        players[i].nextMove.speed = SPEED_SURGE;
        players[i].nextMove.intent = INTENT_SURGE;
        // Check straight
        //
        var shouldGoStraight = true;
        var pointStraight = new Point(players[i].x + BASE_VELOCITY*(1-SURGE_RATIO)*2, players[i].y);
        for (var j = 0; j < numPlayers; j++) {
          if (i != j) {
            var distance = orthogonalDistance(pointStraight, players[i].position);
            if (distance < 2*PLAYER_RADIUS + MIN_SURGE_AVOID_DISTANCE) {
              shouldGoStraight = false;
              break;
            }
          }
        }
        if (shouldGoStraight) {
          players[i].nextMove.position = DIRECTION_STRAIGHT;
          continue;
        }
        
        // Check left, right
        //
        var pointLeft = new Point(pointStraight.x, pointStraight.y + PLAYER_RADIUS*2);
        var pointRight = new Point(pointStraight.x, pointStraight.y - PLAYER_RADIUS*2);
        var shouldGoLeft = true;
        var shouldGoRight = true;
        for (var j = 0; j < numPlayers; j++) {
          if (i != j) {
            var distanceLeft = orthogonalDistance(pointLeft, players[i].position);
            var distanceRight = orthogonalDistance(pointRight, players[i].position);
            if (distanceLeft < 2*PLAYER_RADIUS + MIN_SURGE_AVOID_DISTANCE) {
              shouldGoLeft = false;
            }
            if (distanceRight < 2*PLAYER_RADIUS + MIN_SURGE_AVOID_DISTANCE) {
              shouldGoRight = false;
            }
          }
        }
        if (shouldGoRight && !shouldGoLeft) {
          players[i].nextMove.direction = DIRECTION_RIGHT;
        } else if (shouldGoLeft && !shouldGoRight) {
          players[i].nextMove.DIRECTION_LEFT;
        } else {
          // Nowhere to go, choose randomly, remove intent for next step
          //
          players[i].nextMove.intent = INTENT_DRAFT;
          if (Math.random() < 0.5) {
            players[i].nextMove.direction = DIRECTION_RIGHT;
          } else {
            players[i].nextMove.direction = DIRECTION_LEFT;
          }
        }
        players[i]._log += "Move=Surge,";
        continue;
        
        
      }
    }
    // Look for best potential to draft
    //
    var bestMove = new  Move(SPEED_BASE, DIRECTION_STRAIGHT, INTENT_DRAFT);
    var bestMoveDistanceSquared = 0;
    for (var j = 0; j < numPlayers; j++) {
      if (i != j) {
        // Player must be ahead
        //
        if (players[i].position.x < players[j].position.x) {
          var targetPosition = new Point(players[j].position.x - 2*PLAYER_RADIUS, players[j].position.y);
          
          var moveDistanceSquared = distanceSquared(players[i].position, targetPosition);
          
          if (!bestMoveDistanceSquared || moveDistanceSquared < bestMoveDistanceSquared) {
            var dx = targetPosition.x - players[i].position.x;
            var dy = targetPosition.y - players[i].position.y;
            
            if (dx > MIN_TARGET_DISTANCE && players[i].energy >= 1) {
              bestMove.speed = SPEED_SURGE;
            } else if (dx < -MIN_TARGET_DISTANCE) {
              bestMove.speed = SPEED_SLOW;
            } else {
              bestMove.speed = SPEED_BASE;
            }
            
            if (dy > MIN_TARGET_DISTANCE) {
              bestMove.direction = DIRECTION_LEFT;
            } else if (dy < -MIN_TARGET_DISTANCE) {
              bestMove.direction = DIRECTION_RIGHT;
            } else {
              bestMove.direction = DIRECTION_STRAIGHT;
            }
            
            bestMoveDistanceSquared = moveDistanceSquared;
          }
        }
      }
    }
    // Evaluate best move
    //
    var willDraft = false;
    if (bestMoveDistanceSquared) {
      var draftProbabilitySquared = (DRAFT_DECISION_LENGTH*DRAFT_DECISION_LENGTH) / bestMoveDistanceSquared;
      players[i]._log += "DraftProbabilitySquared=" + draftProbabilitySquared + ",";
      players[i]._log += "BestMoveDistanceSquared=" + bestMoveDistanceSquared + ",";
      var rand = Math.random();
      if (rand*rand < draftProbabilitySquared) {
        players[i].nextMove = bestMove;
        willDraft = true;
        players[i]._log += "MoveDirection=" + bestMove.direction;
        players[i]._log += "Move=Intentional drafting,";
      }
    }
    // Default move
    //
    if (!willDraft) {
      var defaultMove = new Move(SPEED_BASE, DIRECTION_STRAIGHT, INTENT_DRAFT);
      players[i].nextMove = defaultMove;
      players[i]._log += "Move=none,";
    }
  }
  
  // Increment next moves
  //
  for (var i = 0; i < numPlayers; i++) {
    
    var velocity = BASE_VELOCITY;
    var thisMove = players[i].nextMove;
    var thisDelta = new Point(0, 0)
    if (thisMove.speed == SPEED_SURGE) {
      var energyToFinish = (FINISH_DISTANCE-players[i].position.x)/BASE_VELOCITY/SURGE_RATIO;
      var extraKickFactor = 1;
      if (energyToFinish < players[i].energy) {
        extraKickFactor = players[i].energy/energyToFinish;
        if (extraKickFactor > MAX_KICK_BOOST) {
          extraKickFactor = MAX_KICK_BOOST;
        }
      }
      velocity = BASE_VELOCITY*SURGE_RATIO*extraKickFactor;
      players[i].energy -= 1*extraKickFactor;
    } else if (thisMove.speed == SPEED_SLOW) {
      velocity = BASE_VELOCITY/SURGE_RATIO;
      players[i].energy += SLOW_ENERGY_GAIN;
    } else if (thisMove.speed == SPEED_FINISHED) {
      var stepsSinceFinished = gameState.currentStep - players[i].finishStep;
      if (stepsSinceFinished <= FINISH_SLOWDOWN_STEPS) {
        velocity = BASE_VELOCITY * (1 - stepsSinceFinished / FINISH_SLOWDOWN_STEPS);
      } else {
        velocity = 0;
      }
    }
    
    if (thisMove.direction == DIRECTION_STRAIGHT) {
      thisDelta.x = velocity;
      thisDelta.y = 0;
    } else if (thisMove.direction == DIRECTION_LEFT) {
      thisDelta.x = velocity*STEER_SLOWDOWN_RATIO;
      thisDelta.y = velocity*STEER_RATIO;
    } else {
      thisDelta.x = velocity*STEER_SLOWDOWN_RATIO;
      thisDelta.y = -velocity*STEER_RATIO;
    }
    
    players[i].position.x += thisDelta.x;
    players[i].position.y += thisDelta.y;
    
    // Stay on road
    if (players[i].position.y < -ROAD_WIDTH/2) {
      players[i].position.y = -ROAD_WIDTH/2;
    } else if (players[i].position.y > ROAD_WIDTH/2) {
      players[i].position.y = ROAD_WIDTH/2;
    }
    
    
    
  }
  
  // Resolve next moves
  //
  for (var i = 0; i < numPlayers; i++) {
    // Default move takes precedence
    //
    if (players[i].nextMove.speed == SPEED_BASE && players[i].nextMove.direction == DIRECTION_STRAIGHT) {
      continue;
    }
    
    for (var j = 0; j < numPlayers; j++) {
      if (i != j) {
        var thisDistanceSquared = distanceSquared(players[i].position, players[j].position);
        if (thisDistanceSquared < PLAYER_RADIUS*2) {
          var thisDistance = Math.sqrt(thisDistanceSquared);
          var repelDistance = PLAYER_RADIUS*2 - thisDistance;
          var dx = players[i].position.x - players[j].position.x;
          var dy = players[i].position.y - players[j].position.y;
          if (thisDistance != 0) {
            players[i].contactDirection.x = players[i].contactDirection.x + dx/thisDistance*repelDistance;
            players[i].contactDirection.y = players[i].contactDirection.y + dy/thisDistance*repelDistance;
          }
            
        }
      }
    }
    
    
  }
  
  // Move players
  //
  for (var i = 0; i < numPlayers; i++) {
    players[i].position.x = players[i].position.x + players[i].contactDirection.x;
    players[i].position.y = players[i].position.y + players[i].contactDirection.y;
    players[i].contactDirection = new Point(0, 0);
  }
  
  // Calculate draft
  //
  for (var i = 0; i < numPlayers; i++) {
    for (var j = 0; j < numPlayers; j++) {
      if (i != j) {
        if (players[i].position.x <= players[j].position.x) {
          dx = players[j].position.x - players[i].position.x - PLAYER_RADIUS - MIN_SURGE_AVOID_DISTANCE;
          if (dx < 0) { dx = 0; }
          if (dx < DRAFT_LENGTH) {
            dy = Math.abs(players[j].position.y - players[i].position.y);
            if (dy < DRAFT_WIDTH/2) {
              var draftRatio = (DRAFT_WIDTH/2 + DRAFT_LENGTH - dx - dy) / (DRAFT_WIDTH/2 + DRAFT_LENGTH);
              var energyAdd = draftRatio*DRAFT_ENERGY_RATIO;
              players[i].energy += energyAdd;
            }
          }
        }
      }
    }
  }
  
  // Check who is finished
  //
  var newNumFinished = numFinished;
  for (var i = 0; i < numPlayers; i++) {
    if (!players[i].finished && players[i].position.x >= FINISH_DISTANCE) {
      players[i].finished = true;
      players[i].finishStep = gameState.currentStep;
      newNumFinished++;
      players[i].rank = newNumFinished;
    }
  }
  
  return newNumFinished;
  
  
}


var METER_WIDTH = 600;

function animate() {
  var players = gameState.racePlayers;
  var numPlayers = players.length;
  // Re-center horizontally around player #10
  //
  globalViewAttributes.gameCenter.x = players[gameState.userPlayerIndex].position.x;
  // Position background
  //
  for (var i = 0; i < gameState.raceInfo.background.length; i++) {
    gameState.raceInfo.background[i].render(gameState.gameWindow);
  }

  // Position players
  //
  for (var i = 0; i < numPlayers; i++) {
  
  
    
    var cadence = 1;
    if (players[i].nextMove.speed == SPEED_SURGE) {
      cadence = SURGE_RATIO;
    } else if (players[i].nextMove.speed == SPEED_SLOW) {
      cadence = 1/SURGE_RATIO;
    } else if (players[i].nextMove.speed == SPEED_FINISHED) {
      var stepsSinceFinished = gameState.currentStep - players[i].finishStep;
      if (stepsSinceFinished <= FINISH_SLOWDOWN_STEPS) {
        cadence = (1 - stepsSinceFinished / FINISH_SLOWDOWN_STEPS);
      } else {
        cadence = 0;
      }

    }
    players[i].incrementStride(SIM_STEP_TIME_MS, cadence);
    
    
    
    players[i].render(gameState.gameWindow);
    
    
  }
  
  // Update info bar
  //
  var distanceRatio = players[gameState.userPlayerIndex].position.x / FINISH_DISTANCE;
  var distancePercent = Math.floor(distanceRatio*100);
  document.getElementById("distancePercent").innerHTML = distancePercent;
  
  var distanceMeterWidth = Math.floor(distanceRatio*METER_WIDTH);
  document.getElementById("distanceMeterFill").style.width = distanceMeterWidth;
  
  var rank = getPlayerRank(gameState.userPlayerIndex);
  
  var rankDisplay = getOrdinal(rank);
  document.getElementById("rank").innerHTML = rankDisplay;
  
  var userEnergy = players[gameState.userPlayerIndex].energy;
  var ENERGY_DISPLAY_RATIO = 1;
  var energyMeterWidth = userEnergy*ENERGY_DISPLAY_RATIO;
  document.getElementById("energyMeterFill").style.width = energyMeterWidth;
  
  
}

var SPRITE_FRAME_RATE=25;
var SPRITE_FRAME_TIME_MS = 1000/SPRITE_FRAME_RATE;

function refreshSprites() {
  console.log("refreshSprites");
  var startTime = new Date();
  var players = gameState.racePlayers;
  var numPlayers = players.length;
  for (var i = 0; i < numPlayers; i++) {
    players[i].refreshSprite();
    
    
  }
  var endTime = new Date();
  
  var durationMs = endTime.getTime() - startTime.getTime();
  
  var waitTime = SPRITE_FRAME_TIME_MS - durationMs;
  while (waitTime < 0) {
    waitTime += SPRITE_FRAME_TIME_MS;
  }
//  if (waitTime < 0) { waitTime = 0; }
  
  setTimeout("refreshSprites()", waitTime);

}

function getPlayerRank(playerIndex) {
  var players = gameState.racePlayers;
  var numPlayers = players.length;
  var playerFinished = players[playerIndex].finished;
  var playerX = players[playerIndex].position.x;
  var playerFinishStep = players[playerIndex].finishStep;
  var rank = 1;
  for (i = 0; i < numPlayers; i++) {
    if (i != playerIndex) {
      if (playerFinished) {
        if (players[i].finished) {
          if (players[i].finishStep < playerFinishStep) {
            rank++;
          }
        }
      } else {
        if (players[i].position.x > playerX) {
          rank++;
        }
      }
    }
  }
  return rank;
}


function rgb(r, g, b) {
  return "rgb("+r+","+g+","+b+")";
}

function getOrdinal(n) {
  var ordinal;
  if (n % 10 == 1) {
    ordinal = n + "st";
  } else if (n % 10 == 2) {
    ordinal = n + "nd";
  } else if (n % 10 == 3) {
    ordinal = n + "rd";
  } else {
    ordinal = n + "th";
  }
  return ordinal;
}

function rand256() {
  return Math.floor(Math.random()*256);
}



function distanceSquared(pointA, pointB) {
  var dx = pointA.x - pointB.x;
  var dy = pointA.y - pointB.y;
  var dSquared = dx*dx + dy*dy;
  return(dSquared);
}

function orthogonalDistance(pointA, pointB) {
  var dx = Math.abs(pointA.x - pointB.x);
  var dy = Math.abs(pointA.y - pointB.y);
  var dOrthogonal = dx + dy;
  return(dOrthogonal);
}
