import kol.Error as Error
from GenericRequest import GenericRequest
from kol.manager import PatternManager
from kol.util import ParseResponseUtils

class DrinkBoozeRequest(GenericRequest):
    """
    This class is for drinking booze from the inventory.
    It accepts the current session and the ID number of the booze to be drank.
    It returns the results, including and stat gain, adventure gain,
    effect gain, or drunkenness gain.
    """

    def __init__(self, session, boozeId):
        super(DrinkBoozeRequest, self).__init__(session)
        self.url = session.serverURL + "inv_booze.php?pwd=" + session.pwd + "&which=1&whichitem=" + str(boozeId)

    def parseResponse(self):
        # Check for errors
        tooDrunkPattern = PatternManager.getOrCompilePattern('tooDrunk')
        if tooDrunkPattern.search(self.responseText):
            raise Error.Error("You are too drunk to drink more booze.", Error.USER_IS_DRUNK)
        notBoozePattern = PatternManager.getOrCompilePattern('notBooze')
        if notBoozePattern.search(self.responseText):
            raise Error.Error("That item is not booze.", Error.WRONG_KIND_OF_ITEM)
        boozeMissingPattern = PatternManager.getOrCompilePattern('notEnoughItems')
        if boozeMissingPattern.search(self.responseText):
            raise Error.Error("Item not in inventory.", Error.ITEM_NOT_FOUND)

        # Check the results
        results = {}
        results["drunkenness"] = ParseResponseUtils.parseDrunkGained(self.responseText)
        results["adventures"] = ParseResponseUtils.parseAdventuresGained(self.responseText)

        substats = ParseResponseUtils.parseSubstatsGainedLost(self.responseText)
        if len(substats) > 0:
            results["substats"] = substats
        stats = ParseResponseUtils.parseStatsGainedLost(self.responseText)
        if len(stats) > 0:
            results["stats"] = stats
        level = ParseResponseUtils.parseLevelsGained(self.responseText)
        if level != 0:
            results["level"] = level
        hp = ParseResponseUtils.parseHPGainedLost(self.responseText)
        if hp != 0:
            results["hp"] = hp
        mp = ParseResponseUtils.parseMPGainedLost(self.responseText)
        if mp != 0:
            results["mp"] = mp
        effects = ParseResponseUtils.parseEffectsGained(self.responseText)
        if len(effects) > 0:
            results["effects"] = effects

        self.responseData = results

