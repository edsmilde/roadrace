
var EFFECTIVE_DISTANCE_RATIO = 0.5;
function getEffectiveDistance(distanceInMeters) {
  return distanceInMeters * EFFECTIVE_DISTANCE_RATIO;
}

var DEFAULT_SPRITE_OFFSET = {"x": 0, "y": 0};

function renderSelectedBackground(backgroundPieces, gameWindow) {
  for (var i = 0; i < backgroundPieces.length; i++) {
    backgroundPieces[i].render(gameWindow);
  }
}

  
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

function heightToScreenVertical(height) {
  return height * globalViewAttributes.scale.z;
}


function BackgroundPiece(position, width, height, spritePath, zIndex, spriteOffset, vertical=false) {
    this.position = position;
    this.width = width;
    this.height = height;
    this.spritePath = spritePath;
    this.created = false;
    this.zIndex = zIndex;
    this.element = null;
    this.opacity = 1;
    this.spriteOffset = spriteOffset;
    this.vertical = vertical;
    this.render = function(screenElement) {
      var screenPosition = pointToScreen(this.position);
      screenPosition.x = screenPosition.x - widthToScreen(this.spriteOffset.x);
      if (this.vertical) {
        screenPosition.y = screenPosition.y - heightToScreenVertical(this.spriteOffset.y);
      } else {
        screenPosition.y = screenPosition.y - heightToScreen(this.spriteOffset.y);
      }
      var screenWidth = widthToScreen(width);
      var screenHeight;
      if (this.vertical) {
        screenHeight = heightToScreenVertical(height);
      } else {
        screenHeight = heightToScreen(height);
      }
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



function getRoadBackgroundNoEdges(finishDistance, roadType, landType) {
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



function getRoadSection(startDistance, finishDistance, roadType) {
  var backgroundPieces = new Array();
  // Create road
  //
  // Center road pieces
  //
  var roadStartLeft = startDistance;
  var roadStartTop = -100;
  var roadBlockHeight = 50;
  var roadBlockWidth = 50;

  var roadEndRight = finishDistance;
  var roadEndBottom = 100;

  for (var left = roadStartLeft; left < roadEndRight; left += roadBlockWidth) {
      for (var top = roadStartTop; top < roadEndBottom; top += roadBlockHeight) {
      var thisPosition = new Point(left, top);
      var thisSprite = getGroundSpritePath(roadType, "center");
      var thisPiece = new BackgroundPiece(thisPosition, roadBlockWidth, roadBlockWidth, thisSprite, -1001, DEFAULT_SPRITE_OFFSET);
      backgroundPieces.push(thisPiece);
      }
  }
  return backgroundPieces;
}




function getRoadSectionWithEdges(startDistance, finishDistance, roadType) {
  var backgroundPieces = new Array();
  // Create road
  //
  // Center road pieces
  //
  var roadStartLeft = startDistance;
  var roadStartTop = -100;
  var roadBlockHeight = 50;
  var roadBlockWidth = 50;

  var roadEndRight = finishDistance;
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
  return backgroundPieces;
}

function getRoadBackgroundSection(startDistance, finishDistance, landType) {
  var backgroundPieces = new Array();
  // Create road
  //
  // Center road pieces
  //
  var roadStartLeft = startDistance;
  var roadStartTop = -100;
  var roadEndRight = finishDistance;
  var roadEndBottom = 100;
  
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

  return backgroundPieces;  
}



function getStartAndFinishPieces(finishDistance) {
  var backgroundPieces = new Array();

  var roadStartTop = -100;
  var roadEndBottom = 100;
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

function getAsphaltSandRoadBackground(finishDistance) {
  return getRoadBackground(finishDistance, "asphalt", "sand");
}

function getAsphaltPrarieRoadBackground(finishDistance) {
  return getRoadBackground(finishDistance, "asphalt", "prairie");
}

function getBrickGrassRoadBackground(finishDistance) {
  return getRoadBackgroundNoEdges(finishDistance, "brick", "grass");
}

var TREE_SPRITE_BASE = "sprites/objects/trees/"

var TREE_SIZE_DECIDUOUS = {"width": 100, "height": 140}
var TREE_SPRITE_OFFSET_DECIDUOUS = {"x": 50, "y": 130};
var NUM_TREE_SPRITES_DECIDUOUS = 30;

var NUM_TREE_SPRITES_PALM = 30;
var TREE_SIZE_SCALE_PALM = 6;
var TREE_SIZE_PALM = {"width": 10*TREE_SIZE_SCALE_PALM, "height": 14*TREE_SIZE_SCALE_PALM}
var TREE_SPRITE_OFFSET_PALM = {"x": 5*TREE_SIZE_SCALE_PALM, "y": 13*TREE_SIZE_SCALE_PALM};

var TREE_SIZE_EVERGREEN = {"width": 100, "height": 140}
var TREE_SPRITE_OFFSET_EVERGREEN = {"x": 50, "y": 120};
var NUM_TREE_SPRITES_EVERGREEN = 30;



function getTreePiece(x, y, size, spriteOffset, treeType, spriteIndex) {
  var treeSprite = TREE_SPRITE_BASE + treeType + "_" + spriteIndex + ".png";
  var zIndex = y;
  var position = {"x": x, "y": y};
  var treePiece = new BackgroundPiece(position, size.width, size.height, treeSprite, zIndex, spriteOffset, true);
  return treePiece;
}

var BUILDING_SPRITE_BASE = "sprites/objects/buildings/"
var BUILDING_SIZE_RATIO = 1;
var BUILDING_DEFAULT_WIDTH = 200*BUILDING_SIZE_RATIO;
var BUILDING_DEFAULT_HEIGHT = 400*BUILDING_SIZE_RATIO;
function getBuildingPiece(x, y, width, height, buildingType, piece) {
  var sprite = BUILDING_SPRITE_BASE + buildingType + "_" + piece + ".png";
  var zIndex = y;
  var position = {"x": x, "y": y};
  var spriteOffset = {"x": 0, "y": height};
  var piece = new BackgroundPiece(position, width, height, sprite, zIndex, spriteOffset, true);
  return piece;
}

function getBuildingStuccoPiece(x, y, piece) {
  var width = BUILDING_DEFAULT_WIDTH;
  var height = BUILDING_DEFAULT_HEIGHT;
  var buildingType = "stucco";
  return getBuildingPiece(x, y, width, height, buildingType, piece);
}

function getBuildingSequence(x, y, width, height, buildingType, pieces) {
  var backgroundPieces = new Array();
  for (i = 0; i < pieces.length; i ++) {
    var thisX = x + width*i;
    var backgroundPiece = getBuildingPiece(thisX, y, width, height, buildingType, pieces[i])
    backgroundPieces.push(backgroundPiece);
  }
  return backgroundPieces;
}

function getRandomDeciduousTreePiece(x, y) {
  var treeSpriteIndex = Math.floor(Math.random() * NUM_TREE_SPRITES_DECIDUOUS);
  return getTreePiece(x, y, TREE_SIZE_DECIDUOUS, TREE_SPRITE_OFFSET_DECIDUOUS, "deciduous", treeSpriteIndex);
}

function getRandomAutumnTreePiece(x, y) {
  var treeSpriteIndex = Math.floor(Math.random() * NUM_TREE_SPRITES_DECIDUOUS);
  return getTreePiece(x, y, TREE_SIZE_DECIDUOUS, TREE_SPRITE_OFFSET_DECIDUOUS, "autumn", treeSpriteIndex);
}

function getRandomBareTreePiece(x, y) {
  var treeSpriteIndex = Math.floor(Math.random() * NUM_TREE_SPRITES_DECIDUOUS);
  return getTreePiece(x, y, TREE_SIZE_DECIDUOUS, TREE_SPRITE_OFFSET_DECIDUOUS, "bare", treeSpriteIndex);
}

function getRandomPalmTreePiece(x, y) {
  var treeSpriteIndex = Math.floor(Math.random() * NUM_TREE_SPRITES_PALM);
  return getTreePiece(x, y, TREE_SIZE_PALM, TREE_SPRITE_OFFSET_PALM, "palm", treeSpriteIndex);
}

function getRandomEvergreenTreePiece(x, y) {
  var treeSpriteIndex = Math.floor(Math.random() * NUM_TREE_SPRITES_EVERGREEN);
  return getTreePiece(x, y, TREE_SIZE_EVERGREEN, TREE_SPRITE_OFFSET_EVERGREEN, "evergreen", treeSpriteIndex);
}