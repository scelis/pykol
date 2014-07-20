from GenericRequest import GenericRequest
from kol.manager import PatternManager

class ClanWhitelistRequest(GenericRequest):
    "Retrieves information from the clan whitelist page."

    def __init__(self, session):
        super(ClanWhitelistRequest, self).__init__(session)
        self.url = session.serverURL + "clan_whitelist.php"

    def parseResponse(self):
        # Get the set of clan ranks.
        ranks = []
        ranksById = {}
        rankContainerPattern = PatternManager.getOrCompilePattern('clanRankContainer')
        match = rankContainerPattern.search(self.responseText)
        if match:
            rankText = match.group(1)
            rankPattern = PatternManager.getOrCompilePattern('clanRank')
            for rankMatch in rankPattern.finditer(rankText):
                rank = {}
                rank["rankId"] = int(rankMatch.group(1))
                rank["rankName"] = rankMatch.group(2)
                rank["rankNumber"] = int(rankMatch.group(3))
                ranks.append(rank)
                ranksById[rank["rankId"]] = rank

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
            rankNumber = None
            if rankId != None:
                rank = ranksById[int(rankId)]
                member["rankId"] = rank["rankId"]
                member["rankName"] = rank["rankName"]
                member["rankNumber"] = rank["rankNumber"]
            elif rankName != None:
                member["rankName"] = rankName
                foundRank = False
                for rank in ranks:
                    if rank["rankName"] == rankName:
                        foundRank = True
                        break
                if foundRank == False:
                    rank = {}
                    rank["rankId"] = -1
                    rank["rankName"] = rankName
                    rank["rankNumber"] = -1
                    ranks.append(rank)
            members.append(member)

        self.responseData["ranks"] = ranks
        self.responseData["members"] = members

