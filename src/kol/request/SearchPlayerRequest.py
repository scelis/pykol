from GenericRequest import GenericRequest
from kol.manager import PatternManager

STARTSWITH = 1
CONTAINS = 2
ENDSWITH = 3

class SearchPlayerRequest(GenericRequest):
    def __init__(self, session, queryString, queryType=STARTSWITH, pvpOnly=False, hardcoreOnly=None, searchLevel=None, searchRanking=None):
        super(SearchPlayerRequest, self).__init__(session)
        self.url = session.serverURL + "searchplayer.php"
        self.requestData["searchstring"] = queryString
        self.requestData['startswith'] = queryType
        self.requestData['searching'] = 'Yep'

        if pvpOnly:
            self.requestData['pvponly'] = 1

        if hardcoreOnly is not None:
            if hardcoreOnly:
                self.requestData['hardcoreonly'] = 1
            else:
                self.requestData['hardcoreonly'] = 2
        else:
            self.requestData['hardcoreonly'] = 0

        if searchLevel:
            self.requestData['searchlevel'] = searchLevel
        if searchRanking:
            self.requestData['searchranking'] = searchRanking

    def parseResponse(self):
        searchPattern = PatternManager.getOrCompilePattern('searchPlayers')
        players = []
        for player in searchPattern.finditer(self.responseText):
            userId = int(player.group(1))
            name = player.group(2)
            p = { 'userName' : name, 'userId' : userId }
            players.append(p)
        self.responseData['players'] = players
