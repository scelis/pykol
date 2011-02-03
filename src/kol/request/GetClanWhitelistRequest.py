from GenericRequest import GenericRequest
from kol.manager import PatternManager

class GetClanWhitelistRequest(GenericRequest):
    "Adds meat to the player's closet."

    def __init__(self, session, meat=""):
        super(GetClanWhitelistRequest, self).__init__(session)
        self.url = session.serverURL + "clan_whitelist.php"

    def parseResponse(self):
        # Get the set of clan ranks.
        ranks = []
        rankContainerPattern = PatternManager.getOrCompilePattern('clanRankContainer')
        match = rankContainerPattern.search(self.responseText)
        rankText = match.group(1)
        rankPattern = PatternManager.getOrCompilePattern('clanRank')
        for rankMatch in rankPattern.finditer(rankText):
            rank = {}
            rank["id"] = int(rankMatch.group(1))
            rank["name"] = rankMatch.group(2)
            rank["number"] = int(rankMatch.group(3))
            ranks.append(rank)
            print rank
        self.responseData["ranks"] = ranks
