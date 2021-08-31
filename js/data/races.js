

var EFFECTIVE_DISTANCE_RATIO = 0.5;
function getEffectiveDistance(distanceInMeters) {
  return distanceInMeters * EFFECTIVE_DISTANCE_RATIO;
}

var DISTANCE_5K = getEffectiveDistance(5000);
var DISTANCE_10K = getEffectiveDistance(10000);
var DISTANCE_HM = getEffectiveDistance(21097.5);
var DISTANCE_MARATHON = getEffectiveDistance(42195);

function RaceInfo(raceName, distance, description, thumbnail, background, optionalCompetitors, requiredCompetitors, numCompetitors, pointsMultiplier) {
  this.raceName = raceName;
  this.distance = distance;
  this.description = description;
  this.thumbnail = thumbnail;
  this.background = background;
  this.requiredCompetitors = requiredCompetitors;
  this.optionalCompetitors = optionalCompetitors;
  this.numCompetitors = numCompetitors;
  this.pointsMultiplier = pointsMultiplier;
}

var competitorPoolEmpty = new Array();
var competitorPoolSample = new Array();

var roadBackground;

// Hobbyjogger tier races
var raceDemo = new RaceInfo("Demo", DISTANCE_5K, "", "", getBackgroundDemo(DISTANCE_5K), fieldsOptional["FieldDemo"], fieldsRequired["FieldDemo"], 4, 1);
var raceForestPark = new RaceInfo("Forest Park 10K", DISTANCE_10K, "", "", getBackgroundForestPark(DISTANCE_10K), fieldsOptional["FieldA"], fieldsRequired["FieldA"], 9, 3);
var raceGreatPlains = new RaceInfo("Great Plains Turkey Trot", DISTANCE_10K, "", "", getBackgroundGreatPlains(DISTANCE_10K), fieldsOptional["FieldA"], fieldsRequired["FieldA"], 9, 3);
var raceSunsetBeach = new RaceInfo("Sunset Beach 10K", DISTANCE_10K, "", "", getBackgroundSunsetBeach(DISTANCE_10K), fieldsOptional["FieldA"], fieldsRequired["FieldA"], 9, 3);

// Sub-elite tier races
var raceMainStreet = new RaceInfo("Main Street Half", DISTANCE_HM, "", "", getBackgroundMainStreet(DISTANCE_HM), fieldsOptional["FieldA"], fieldsRequired["FieldA"], 9, 3);
var raceMediterranean = new RaceInfo("Mediterranean 10K", DISTANCE_10K, "", "", getBackgroundMediterranean(DISTANCE_10K), fieldsOptional["FieldA"], fieldsRequired["FieldA"], 15, 3);
var raceOldTown = new RaceInfo("Old Town Marathon", DISTANCE_MARATHON, "", "", roadBackground, competitorPoolEmpty, competitorPoolSample, 9, 3);
var raceArcticClassic = new RaceInfo("Arctic Classic Half", DISTANCE_HM, "", "", getBackgroundArctic(DISTANCE_HM), fieldsOptional["FieldA"], fieldsRequired["FieldA"], 15, 3);

// Elite tier races
var raceIslandGames = new RaceInfo("Island Games Marathon", DISTANCE_MARATHON, "", "", getBackgroundIsland(DISTANCE_MARATHON), fieldsOptional["FieldA"], fieldsRequired["FieldA"], 9, 3);
var raceMetroInternational = new RaceInfo("Metro International Marathon", DISTANCE_MARATHON, "", "", roadBackground, competitorPoolEmpty, competitorPoolSample, 9, 3);
var raceGoldenShoe = new RaceInfo("Golden Shoe Half", DISTANCE_HM, "", "", roadBackground, competitorPoolEmpty, competitorPoolSample, 9, 3);
var raceTropicInvitational = new RaceInfo("Tropical Invitational Marathon", DISTANCE_MARATHON, "", "", roadBackground, competitorPoolEmpty, competitorPoolSample, 9, 3);


// Olympics
var raceOlympics = new RaceInfo("Olympic Games", DISTANCE_MARATHON, "", "", roadBackground, competitorPoolEmpty, competitorPoolSample, 9, 3);


function RaceTierInfo(tierName, description, races) {
  this.raceTierName = tierName;
  this.description = description;
  this.races = races;
}

var tierHobbyjogger = new RaceTierInfo("Hobbyjogger", "", [raceDemo, raceForestPark, raceGreatPlains, raceSunsetBeach]);
var tierSubElite = new RaceTierInfo("Sub-Elite", "", [raceMainStreet, raceMediterranean, raceOldTown, raceArcticClassic]);
var tierElite = new RaceTierInfo("Elite", "", [raceIslandGames, raceMetroInternational, raceGoldenShoe, raceTropicInvitational]);
var tierChampionship = new RaceTierInfo("Championship", "", [raceOlympics]);

var raceTiers = [tierHobbyjogger, tierSubElite, tierElite, tierChampionship];







