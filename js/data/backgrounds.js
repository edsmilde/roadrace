
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
    var x = Math.random()*(distance + 200);
    var y = 102 + Math.floor(Math.random() * 50);
    var treePiece = getRandomDeciduousTreePiece(x, y,);
    background.push(treePiece);
  }
  var numTreesTop = 100;
  for (var i = 0; i < numTreesTop; i++) {
    var x = Math.random()*(distance + 200);
    var y = -112 + Math.floor(Math.random() * 8);
//    var y = 105;
    var treePiece = getRandomDeciduousTreePiece(x, y);
    background.push(treePiece);
  }

  return background;
}

function getBackgroundSunsetBeach(distance) {
  var background = getAsphaltSandRoadBackground(distance);

  // Insert trees randomly
  var numTreesBottom = 100;
  for (var i = 0; i < numTreesBottom; i++) {
    var x = Math.random()*(distance + 200);
    var y = 105 + Math.floor(Math.random() * 8);
    var treePiece = getRandomPalmTreePiece(x, y,);
    background.push(treePiece);
  }
  var numTreesTop = 100;
  for (var i = 0; i < numTreesTop; i++) {
    var x = Math.random()*(distance + 200);
    var y = -113 + Math.floor(Math.random() * 8);
//    var y = 105;
    var treePiece = getRandomPalmTreePiece(x, y);
    background.push(treePiece);
  }

  return background;
}

function getBackgroundGreatPlains(distance) {
  var background = getAsphaltPrarieRoadBackground(distance);

  // Insert trees randomly
  var numTreesBottom = 20;
  for (var i = 0; i < numTreesBottom; i++) {
    var x = Math.random()*(distance + 200);
    var y = 105 + Math.floor(Math.random() * 8);
    var treePiece = getRandomAutumnTreePiece(x, y,);
    background.push(treePiece);
  }
  var numTreesTop = 20;
  for (var i = 0; i < numTreesTop; i++) {
    var x = Math.random()*(distance + 200);
    var y = -113 + Math.floor(Math.random() * 8);
//    var y = 105;
    var treePiece = getRandomAutumnTreePiece(x, y);
    background.push(treePiece);
  }



  return background;
}


function getBackgroundMainStreet(distance) {
  //var background = getBrickGrassRoadBackground(distance);

  var land = getRoadBackgroundSection(-100, distance + 200, "grass");
  var brickSectionOne = getRoadSection(-100, distance/5, "brick");
  var asphaltSection = getRoadSectionWithEdges(distance/5, 4*distance/5, "asphalt");
  var brickSectionTwo = getRoadSection(4*distance/5, distance+200, "brick");

  var startFinishPieces = getStartAndFinishPieces(distance);

  var background = land.concat(brickSectionOne).concat(asphaltSection).concat(brickSectionTwo).concat(startFinishPieces);

  return background;
}

function getBackgroundMediterranean(distance) {
  var background = getRoadBackground(distance, "cobble", "limestone");

  var houseA = getBuildingSequence(100, -102, 20, 50, "stucco", ["left", "window", "window", "door", "window", "right"]);
  var houseB = getBuildingSequence(300, 140, 20, 50, "stucco", ["left", "blank", "blank", "blank", "blank", "blank", "right"]);
  var background = background.concat(houseA).concat(houseB);


  return background;
}




function getBackgroundArctic(distance) {
  var background = getRoadBackground(distance, "asphalt", "snow");

  // Insert trees randomly
  var numTreesBottom = 50;
  for (var i = 0; i < numTreesBottom; i++) {
    var x = Math.random()*(distance + 200);
    var y = 105 + Math.floor(Math.random() * 8);
    var treePiece = getRandomBareTreePiece(x, y,);
    background.push(treePiece);
  }
  var numTreesTop = 50;
  for (var i = 0; i < numTreesTop; i++) {
    var x = Math.random()*(distance + 200);
    var y = -113 + Math.floor(Math.random() * 8);
    var treePiece = getRandomBareTreePiece(x, y);
    background.push(treePiece);
  }

  // Evergreens
  numTreesBottom = 50;
  for (var i = 0; i < numTreesBottom; i++) {
    var x = Math.random()*(distance + 200);
    var y = 105 + Math.floor(Math.random() * 8);
    var treePiece = getRandomEvergreenTreePiece(x, y,);
    background.push(treePiece);
  }
  numTreesTop = 50;
  for (var i = 0; i < numTreesTop; i++) {
    var x = Math.random()*(distance + 200);
    var y = -113 + Math.floor(Math.random() * 8);
    var treePiece = getRandomEvergreenTreePiece(x, y);
    background.push(treePiece);
  }
  
  


  var houseLocations = [100, 700, 900, 1300, 1900, 2200, 2900, 3200, 3700, 4100, 4500];
  for (var i = 0; i < houseLocations.length; i++) {
    var house = getBuildingSequence(houseLocations[i], -105, 20, 40, "swedish", ["left", "window", "window", "door", "window", "right"]);
    background = background.concat(house);  
  }
  return background;
}

function getBackgroundIsland(distance) {
  var background = getRoadBackgroundNoEdges(distance, "plank", "water");
  return background;
}
