import kol.Error as Error
from GenericRequest import GenericRequest
from kol.database import ItemDatabase
from kol.manager import PatternManager
from kol.util import ParseResponseUtils
from kol.util import Report

class BarrelRequest(GenericRequest):
    "Opens a Barrel in the Barrel Full of Barrels."

    def __init__(self, session, whichBarrel):
        super(BarrelRequest, self).__init__(session)
        self.session = session
        self.url = session.serverURL + "barrel.php"
        self.requestData['pwd'] = session.pwd
        self.requestData['smash'] = whichBarrel

    def parseResponse(self):
        notBarrelPattern = PatternManager.getOrCompilePattern('usedBarrel')
        noAdventuresPattern = PatternManager.getOrCompilePattern('noAdventures')
        if notBarrelPattern.match(self.responseText):
            raise Error.Error("Barrel already opened or doesn't exist. (#%s)" % self.requestData['smash'], Error.INVALID_ACTION)
        if noAdventuresPattern.match(self.responseText):
            raise Error.Error("You don't have enough adventures to smash that", Error.NOT_ENOUGH_ADVENTURES)

        url = self.response.url
        if url.find("/fight.php") >= 0:
            # Get the monster's name.
            self.responseData["adventureType"] = "combat"
            monsterNamePattern = PatternManager.getOrCompilePattern('monsterName')
            monsterNameMatch = monsterNamePattern.search(self.responseText)
            self.responseData["monsterName"] = monsterNameMatch.group(1)

            # Check to see if the fight was won or lost.
            fightWonPattern = PatternManager.getOrCompilePattern('fightWon')
            if fightWonPattern.search(self.responseText):
                self.responseData["fightWon"] = True
            else:
                fightLostPattern = PatternManager.getOrCompilePattern('fightLost')
                if fightLostPattern.search(self.responseText):
                    self.responseData["fightLost"] = True

            # Get items, meat, and substats gained. We always need to check these since they can
            # happen at any point during the fight.
            self.responseData["items"] = ParseResponseUtils.parseItemsReceived(self.responseText, self.session)
            self.responseData["meat"] = ParseResponseUtils.parseMeatGainedLost(self.responseText)
            self.responseData["substats"] = ParseResponseUtils.parseSubstatsGainedLost(self.responseText)

        item = ParseResponseUtils.parseItemsReceived(self.responseText, self.session)
        if len(item) > 0:
            self.responseData["items"] = item

        hp = ParseResponseUtils.parseHPGainedLost(self.responseText)
        if hp != 0:
            self.responseData["hp"] = hp
