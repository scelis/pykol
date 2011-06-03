from GenericRequest import GenericRequest
from kol.manager import PatternManager

class ClanWhitelistRequest(GenericRequest):
    "Retrieves information from the clan whitelist page."

    def __init__(self, session):
        super(ClanWhitelistRequest, self).__init__(session)
        self.url = session.serverURL + "clan_whitelist.php"

    def parseResponse(self):
        # Get the set of clan ranks.
        ranks = {}
        rankContainerPattern = PatternManager.getOrCompilePattern('clanRankContainer')
        match = rankContainerPattern.search(self.responseText)
        if match:
            rankText = match.group(1)
            rankPattern = PatternManager.getOrCompilePattern('clanRank')
            for rankMatch in rankPattern.finditer(rankText):
                rank = {}
                rank["name"] = rankMatch.group(2)
                rank["number"] = int(rankMatch.group(3))
                ranks[int(rankMatch.group(1))] = rank
            self.responseData["ranks"] = ranks

        # Get a list of users who are whitelisted to the clan.
        members = []
        memberPattern = PatternManager.getOrCompilePattern('clanWhitelistMember')
        for match in memberPattern.finditer(self.responseText):
            member = {}
            member["userId"] = match.group('userId')
            member["userName"] = match.group('userName')
            member["clanTitle"] = match.group('clanTitle')
            rankId = match.group('clanRankId')
            rankName = match.group('clanRankName')
            if rankId != None:
                rank = ranks[int(rankId)]
            elif rankName != None:
                rank = {"name" : rankName}
            member["clanRank"] = rank
            members.append(member)
        self.responseData["members"] = members
