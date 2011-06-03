from GenericRequest import GenericRequest
from kol.manager import PatternManager
from kol.util import Report

from datetime import datetime

CLAN_LOG_UNKNOWN = 0
CLAN_LOG_FAX = 1
CLAN_LOG_ATTACK = 2
CLAN_LOG_WHITELISTED_PLAYER = 3
CLAN_LOG_JOINED_ANOTHER_CLAN = 4
CLAN_LOG_WHITELISTED_IN = 5
CLAN_LOG_STASH_ADD = 6
CLAN_LOG_STASH_REMOVE = 7
CLAN_LOG_MEAT_SPENT_ARMY = 8
CLAN_LOG_CHANGED_RANK = 9
CLAN_LOG_CHANGED_TITLE = 10

class ClanLogRequest(GenericRequest):
    "Retrieves the clan activity log."

    def __init__(self, session):
        super(ClanLogRequest, self).__init__(session)
        self.url = session.serverURL + "clan_log.php"

    def parseResponse(self):
        entries = []
        entryPattern = PatternManager.getOrCompilePattern('clanLogEntry')
        for entryMatch in entryPattern.finditer(self.responseText):
            entry = {}
            date = entryMatch.group('date')
            entry['date'] = datetime.strptime(date, "%m/%d/%y, %I:%M%p")
            entry['userId'] = int(entryMatch.group('userId'))
            entry['userName'] = entryMatch.group('userName')
            action = entryMatch.group('action')
            foundAction = False
            
            if foundAction == False:
                pattern = PatternManager.getOrCompilePattern('clanLogFax')
                match = pattern.match(action)
                if match:
                    foundAction = True
                    entry['type'] = CLAN_LOG_FAX
                    entry['monster'] = match.group('monsterName')

            if foundAction == False:
                pattern = PatternManager.getOrCompilePattern('clanLogAttack')
                match = pattern.match(action)
                if match:
                    foundAction = True
                    entry['type'] = CLAN_LOG_ATTACK
                    entry['clanName'] = match.group('clanName')

            if foundAction == False:
                pattern = PatternManager.getOrCompilePattern('clanLogWhitelistAdd')
                match = pattern.match(action)
                if match:
                    foundAction = True
                    entry['type'] = CLAN_LOG_WHITELISTED_PLAYER
                    entry['targetUserName'] = match.group('userName')
                    entry['targetUserId'] = int(match.group('userId'))

            if foundAction == False:
                pattern = PatternManager.getOrCompilePattern('clanLogPlayerJoinedAnotherClan')
                match = pattern.match(action)
                if match:
                    foundAction = True
                    entry['type'] = CLAN_LOG_JOINED_ANOTHER_CLAN

            if foundAction == False:
                pattern = PatternManager.getOrCompilePattern('clanLogPlayerJoinedClanWhitelist')
                match = pattern.match(action)
                if match:
                    foundAction = True
                    entry['type'] = CLAN_LOG_WHITELISTED_IN

            if foundAction == False:
                pattern = PatternManager.getOrCompilePattern('clanLogStashItemAdd')
                match = pattern.match(action)
                if match:
                    foundAction = True
                    entry['type'] = CLAN_LOG_STASH_ADD
                    entry['itemName'] = match.group('itemName')
                    entry['quantity'] = int(match.group('quantity').replace(',', ''))

            if foundAction == False:
                pattern = PatternManager.getOrCompilePattern('clanLogStashItemRemove')
                match = pattern.match(action)
                if match:
                    foundAction = True
                    entry['type'] = CLAN_LOG_STASH_REMOVE
                    entry['itemName'] = match.group('itemName')
                    entry['quantity'] = int(match.group('quantity').replace(',', ''))

            if foundAction == False:
                pattern = PatternManager.getOrCompilePattern('clanLogMeatSpentArmy')
                match = pattern.match(action)
                if match:
                    foundAction = True
                    entry['type'] = CLAN_LOG_MEAT_SPENT_ARMY
                    entry['meat'] = int(match.group('meat').replace(',', ''))

            if foundAction == False:
                pattern = PatternManager.getOrCompilePattern('clanLogChangedRank')
                match = pattern.match(action)
                if match:
                    foundAction = True
                    entry['type'] = CLAN_LOG_CHANGED_RANK
                    entry['targetUserName'] = match.group('userName')
                    entry['targetUserId'] = int(match.group('userId'))

            if foundAction == False:
                pattern = PatternManager.getOrCompilePattern('clanLogChangedTitle')
                match = pattern.match(action)
                if match:
                    foundAction = True
                    entry['type'] = CLAN_LOG_CHANGED_RANK
                    entry['targetUserName'] = match.group('userName')
                    entry['targetUserId'] = int(match.group('userId'))
                    entry['clanTitle'] = match.group('clanTitle')

            if foundAction == False:
                Report.error("request", "Unknown clan log action: %s" % action)
                entry['type'] = CLAN_LOG_UNKNOWN
                entry['action'] = action

            entries.append(entry)

        self.responseData["entries"] = entries
