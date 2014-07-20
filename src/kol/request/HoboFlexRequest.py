from GenericRequest import GenericRequest
from kol.util import ParseResponseUtils

class HoboFlexRequest(GenericRequest):
    "Uses the Hobo-Flex Workout Gym to increase the user's muscle."
    def __init__(self, session, numTurns):
        super(HoboFlexRequest, self).__init__(session)
        self.url = session.serverURL + 'clan_rumpus.php'
        self.requestData['preaction'] = 'gym'
        self.requestData['whichgym'] = '3'
        self.requestData['numturns'] = numTurns

    def parseResponse(self):
        self.responseData["substats"] = ParseResponseUtils.parseSubstatsGainedLost(self.responseText, checkMysticality=False, checkMoxie=False)
        self.responseData["stats"] = ParseResponseUtils.parseStatsGainedLost(self.responseText, checkMysticality=False, checkMoxie=False)
        self.responseData["level"] = ParseResponseUtils.parseLevelsGained(self.responseText)
