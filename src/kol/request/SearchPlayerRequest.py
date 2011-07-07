from GenericRequest import GenericRequest
from kol.manager import PatternManager

class SearchPlayerRequest(GenericRequest):
    def __init__(self, session, name):
        super(SearchPlayerRequest, self).__init__(session)
	self.url = session.serverURL + "searchplayer.php"
        self.requestData["searchstring"] = name 
	self.requestData['searching'] = 'Yep'
    
    def parseResponse(self):
	

	searchPattern = PatternManager.getOrCompilePattern('searchPlayers')

	players = []
	
	for player in searchPattern.finditer(self.responseText):
		userId = int(player.group(1))
		name = player.group(2)

		p = { 'userName' : name, 'userId' : userId }

		players.append(p)

	self.responseData['players'] = players



