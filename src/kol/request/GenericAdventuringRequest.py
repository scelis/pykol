import kol.Error as Error
from GenericRequest import GenericRequest
from kol.manager import PatternManager
from kol.util import ParseResponseUtils

class GenericAdventuringRequest(GenericRequest):
    """
    A base class used for common adventuring functionality. Other request classes related to
    adventuring should probably extend this one.
    """

    def parseResponse(self):
        """
        Default response method for adventuring.
        """

        shouldNotBeHerePattern = PatternManager.getOrCompilePattern('userShouldNotBeHere')
        if shouldNotBeHerePattern.search(self.responseText):
            raise Error.Error("Unable to adventure. You should not be here.", Error.INVALID_LOCATION)

        url = self.response.geturl()
        if url.find("/fight.php") >= 0:
            # See if the user tried to perform an invalid action.
            twiddlingThumbsPattern = PatternManager.getOrCompilePattern('twiddlingThumbs')
            if twiddlingThumbsPattern.search(self.responseText):
                raise Error.Error("Could not perform action. Thumbs were twiddled.", Error.INVALID_ACTION)

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

            # The same goes for HP and MP
            self.responseData["hp"] = ParseResponseUtils.parseHPGainedLost(self.responseText)
            self.responseData["mp"] = ParseResponseUtils.parseMPGainedLost(self.responseText)

        elif url.find("/choice.php") >= 0:
            self.responseData["adventureType"] = "choice"
            choiceIdentifierPattern = PatternManager.getOrCompilePattern('choiceIdentifier')
            choiceIdentifierMatch = choiceIdentifierPattern.search(self.responseText)
            if choiceIdentifierMatch:
                choiceNamePattern = PatternManager.getOrCompilePattern('choiceName')
                self.responseData["choiceId"] = choiceIdentifierMatch.group(1)
                self.responseData["choiceName"] = choiceNamePattern.search(self.responseText).group(1)
            else:
                self.responseData["items"] = ParseResponseUtils.parseItemsReceived(self.responseText, self.session)
                self.responseData["meat"] = ParseResponseUtils.parseMeatGainedLost(self.responseText)
                self.responseData["substats"] = ParseResponseUtils.parseSubstatsGainedLost(self.responseText)

        elif url.find("/adventure.php") >= 0:
            self.responseData["adventureType"] = "noncombat"
            noncombatNamePattern = PatternManager.getOrCompilePattern('noncombatName')
            noncombatNameMatch = noncombatNamePattern.search(self.responseText)
            if noncombatNameMatch:
                self.responseData["noncombatName"] = noncombatNameMatch.group(1)
            self.responseData["items"] = ParseResponseUtils.parseItemsReceived(self.responseText, self.session)
            self.responseData["meat"] = ParseResponseUtils.parseMeatGainedLost(self.responseText)
            self.responseData["substats"] = ParseResponseUtils.parseSubstatsGainedLost(self.responseText)
        else:
            raise Error.Error("Adventure URL not recognized: %s" % url, Error.REQUEST_GENERIC)
