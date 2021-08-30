
var DEFAULT_SPRITE_OFFSET = {"x": 0, "y": 0};

  
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




function BackgroundPiece(position, width, height, spritePath, zIndex, spriteOffset) {
    this.position = position;
    this.width = width;
    this.height = height;
    this.spritePath = spritePath;
    this.created = false;
    this.zIndex = zIndex;
    this.element = null;
    this.opacity = 1;
    this.spriteOffset = spriteOffset;
    this.render = function(screenElement) {
      var screenPosition = pointToScreen(this.position);
      screenPosition.x = screenPosition.x - widthToScreen(this.spriteOffset.x);
      screenPosition.y = screenPosition.y - heightToScreen(this.spriteOffset.y);
      var screenWidth = widthToScreen(width);
      var screenHeight = heightToScreen(height);
      if (screenPositionVisible(screenPosition, screenWidth, screenHeight)) {
        if (!this.created) {
          this.element = document.createElement("img");
          this.element.setAttribute("src", spritePath);
          this.element.style.width = screenWidth;
          this.element.style.height = screenHeight;
          this.element.style.position = "absolute";
          this.element.style.zIndex = this.zIndex + globalViewAttributes.zIndexOffset;
          this.element.style.opacity = this.opacity;
        }
        this.element.style.left = screenPosition.x;
        this.element.style.top = screenPosition.y;
        if (!this.created) {
          screenElement.appendChild(this.element);
          this.created = true;
        }
      } else if (this.created) {
        this.hide();
      }
    };
    this.setOpacity = function (opacity) {
      this.opacity = opacity;
    }
    this.hide = function() {
      if (this.element != null) {
        this.element.style.display = "none";
        this.element.remove();  
      }
      this.created = false;
    }
}
  

var SPRITES_PATH_BASE = "sprites/";
var GROUND_SPRITES_PATH_BASE = SPRITES_PATH_BASE + "ground/";

function getGroundSpritePath(surface, position) {
  return GROUND_SPRITES_PATH_BASE + surface + "_" + position + ".png";
}

var LINE_SPRITES_PATH_BASE = SPRITES_PATH_BASE + "lines/";

function getLineSpritePath(line) {
  return LINE_SPRITES_PATH_BASE + line + ".png";
}
  
  

// Generate backgrounds

function getRoadBackground(finishDistance, roadType, landType) {
    var backgroundPieces = new Array();
    // Create road
    //
    // Center road pieces
    //
    var roadStartLeft = -100;
    var roadStartTop = -100;
    var roadBlockHeight = 50;
    var roadBlockWidth = 50;

    var roadEndRight = finishDistance+200;
    var roadEndBottom = 100;

    for (var left = roadStartLeft; left < roadEndRight; left += roadBlockWidth) {
        for (var top = roadStartTop; top < roadEndBottom; top += roadBlockHeight) {
        var thisPosition = new Point(left, top);
        var thisSprite = getGroundSpritePath(roadType, "center");
        var thisPiece = new BackgroundPiece(thisPosition, roadBlockWidth, roadBlockWidth, thisSprite, -1001, DEFAULT_SPRITE_OFFSET);
        backgroundPieces.push(thisPiece);
        }
    }

    // Road edges
    //
    var roadEdgeHeight = 2.5;
    for (var left = roadStartLeft; left < roadEndRight; left += roadBlockWidth) {
        // Top
        //
        var thisTopPosition = new Point(left, roadStartTop - roadEdgeHeight);
        var thisTopSprite = getGroundSpritePath(roadType, "top");
        thisTopPiece = new BackgroundPiece(thisTopPosition, roadBlockWidth, roadEdgeHeight, thisTopSprite, -1001, DEFAULT_SPRITE_OFFSET);
        backgroundPieces.push(thisTopPiece);
        var thisBottomPosition = new Point(left, roadEndBottom);
        var thisBottomSprite = getGroundSpritePath(roadType, "bottom");
        var thisBottomPiece = new BackgroundPiece(thisBottomPosition, roadBlockWidth, roadEdgeHeight, thisBottomSprite, -1001, DEFAULT_SPRITE_OFFSET);
        backgroundPieces.push(thisBottomPiece);
        
    }

    // Create backdrop
    //
    var grassBlockHeight = 100;
    var grassBlockWidth = 100;
    var grassAboveTop = roadStartTop - grassBlockHeight;
    var grassBelowTop = roadEndBottom;
    for (var left = roadStartLeft; left < roadEndRight; left += grassBlockWidth) {
        // Above
        //
        var thisAbovePosition = new Point(left, grassAboveTop);
        var thisBelowPosition = new Point(left, grassBelowTop);
        var thisSprite = getGroundSpritePath(landType, "center")
        var thisAbovePiece = new BackgroundPiece(thisAbovePosition, grassBlockWidth, grassBlockHeight, thisSprite, -1002, DEFAULT_SPRITE_OFFSET);
        var thisBelowPiece = new BackgroundPiece(thisBelowPosition, grassBlockWidth, grassBlockHeight, thisSprite, -1002, DEFAULT_SPRITE_OFFSET);
        backgroundPieces.push(thisAbovePiece);
        backgroundPieces.push(thisBelowPiece);
        
        
        
    }

    // Start/finish lines
    //
    var roadHeight = roadEndBottom - roadStartTop;
    var lineRatio = 20;
    var lineWidth = roadHeight/lineRatio * globalViewAttributes.scale.x / globalViewAttributes.scale.y;

    var startLinePosition = new Point(0, roadStartTop);
    var finishLinePosition = new Point(finishDistance, roadStartTop);

    var startLinePiece = new BackgroundPiece(startLinePosition, lineWidth, roadHeight, getLineSpritePath('start'), -1000, DEFAULT_SPRITE_OFFSET);
    var finishLinePiece = new BackgroundPiece(finishLinePosition, lineWidth, roadHeight, getLineSpritePath('finish'), -1000, DEFAULT_SPRITE_OFFSET);

    startLinePiece.setOpacity(0.5);
    finishLinePiece.setOpacity(0.5);


    backgroundPieces.push(startLinePiece);
    backgroundPieces.push(finishLinePiece);

    return backgroundPieces;
}

function getAsphaltGrassRoadBackground(finishDistance) {
    return getRoadBackground(finishDistance, "asphalt", "grass");
}


var TREE_SPRITE_BASE = "sprites/objects/trees/"
var TREE_DEFAULT_SIZE = {"width": 150, "height": 210}
var TREE_SPRITE_OFFSET = {"x": 75, "y": 195};

function getTreePiece(x, y, spriteIndex) {
  var treeSprite = TREE_SPRITE_BASE + spriteIndex + ".png";
  var zIndex = globalViewAttributes.zIndexOffset + y;
  var position = {"x": x, "y": y};
  var treePiece = new BackgroundPiece(position, TREE_DEFAULT_SIZE.width, TREE_DEFAULT_SIZE.height, treeSprite, zIndex, TREE_SPRITE_OFFSET);
  return treePiece;
}


var NUM_TREE_SPRITES = 30;

function getRandomTreePiece(x, y) {
  var treeSpriteIndex = Math.floor(Math.random() * NUM_TREE_SPRITES);
  return getTreePiece(x, y, treeSpriteIndex);
}


// Get backgrounds

function getBackgroundDemo(distance) {
  var background = getAsphaltGrassRoadBackground(distance);
  return background;
}

function getBackgroundForestPark(distance) {
  var background = getAsphaltGrassRoadBackground(distance);
  // Insert trees randomly
  var numTreesBottom = 100;
  for (var i = 0; i < numTreesBottom; i++) {
    var x = Math.random()*distance;
    var y = 102 + Math.floor(Math.random() * 50);
    var treePiece = getRandomTreePiece(x, y);
    background.push(treePiece);
  }
  var numTreesTop = 100;
  for (var i = 0; i < numTreesBottom; i++) {
    var x = Math.random()*distance;
    var y = -112 + Math.floor(Math.random() * 10);
//    var y = 105;
    var treePiece = getRandomTreePiece(x, y);
    background.push(treePiece);
  }

  return background;
}


function renderSelectedBackground(backgroundPieces, gameWindow) {
  for (var i = 0; i < backgroundPieces.length; i++) {
    backgroundPieces[i].render(gameWindow);
  }
}

