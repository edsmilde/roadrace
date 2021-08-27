
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



