from GenericRequest import GenericRequest
from kol.manager import PatternManager

class SearchPlayerRequest(GenericRequest):
    def __init__(self, session, queryString, queryType=None, pvpOnly=False, HCOnly=None, searchLevel=None, searchRanking=None ):
        super(SearchPlayerRequest, self).__init__(session)
	self.url = session.serverURL + "searchplayer.php"
        self.requestData["searchstring"] = queryString
	self.requestData['searching'] = 'Yep'
	if queryType is not None:
		if queryType == 1 or queryType == 'startswith':
			self.requestData['startswith'] = 1
		elif queryType == 2 or queryType == 'contains':
			self.requestData['startswith'] = 2
		elif queryType == 3 or queryType == 'endswith':
			self.requestData['startswith'] = 3
		else:
			raise ValueError("queryType must be 1, 'startswith', 2, 'contains', 3, 'endswith'. received: %s" % queryType)
	else:
		self.requestData['startswith'] = 1

	if pvpOnly:
		self.requestData['pvponly'] = 1

	if HCOnly is not None:
		if HCOnly:
			self.requestData['hardcoreonly'] = 1
		elif not HCOnly:
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



