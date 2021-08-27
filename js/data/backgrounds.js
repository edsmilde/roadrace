


function BackgroundPiece(position, width, height, spritePath, zIndex) {
    this.position = position;
    this.width = width;
    this.height = height;
    this.spritePath = spritePath;
    this.created = false;
    this.zIndex = zIndex;
    this.element = null;
    this.opacity = 1;
    this.render = function(screenElement) {
      var screenPosition = pointToScreen(this.position);
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
      this.element.style.display = "none";
      this.element.remove();
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
        var thisPiece = new BackgroundPiece(thisPosition, roadBlockWidth, roadBlockWidth, thisSprite, -1001);
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
        thisTopPiece = new BackgroundPiece(thisTopPosition, roadBlockWidth, roadEdgeHeight, thisTopSprite, -1001);
        backgroundPieces.push(thisTopPiece);
        var thisBottomPosition = new Point(left, roadEndBottom);
        var thisBottomSprite = getGroundSpritePath(roadType, "bottom");
        var thisBottomPiece = new BackgroundPiece(thisBottomPosition, roadBlockWidth, roadEdgeHeight, thisBottomSprite, -1001);
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
        var thisAbovePiece = new BackgroundPiece(thisAbovePosition, grassBlockWidth, grassBlockHeight, thisSprite, -1002);
        var thisBelowPiece = new BackgroundPiece(thisBelowPosition, grassBlockWidth, grassBlockHeight, thisSprite, -1002);
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

    var startLinePiece = new BackgroundPiece(startLinePosition, lineWidth, roadHeight, getLineSpritePath('start'), -1000);
    var finishLinePiece = new BackgroundPiece(finishLinePosition, lineWidth, roadHeight, getLineSpritePath('finish'), -1000);

    startLinePiece.setOpacity(0.5);
    finishLinePiece.setOpacity(0.5);


    backgroundPieces.push(startLinePiece);
    backgroundPieces.push(finishLinePiece);

    return backgroundPieces;
}

function getAsphaltGrassRoadBackground(finishDistance) {
    return getRoadBackground(finishDistance, "asphalt", "grass");
}


// Get backgrounds

function getBackgroundDemo() {
    var background = getAsphaltGrassRoadBackground(5000);
    return background;
}


function renderSelectedBackground(backgroundPieces, gameWindow) {
    for (var i = 0; i < backgroundPieces.length; i++) {
      backgroundPieces[i].render(gameWindow);
    }  
}

