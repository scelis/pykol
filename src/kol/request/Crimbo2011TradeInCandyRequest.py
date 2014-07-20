import kol.Error as Error
from GenericRequest import GenericRequest
from kol.manager import PatternManager

class Crimbo2011TradeInCandyRequest(GenericRequest):
    def __init__(self, session, itemId, quantity):
        super(Crimbo2011TradeInCandyRequest, self).__init__(session)
        self.url = session.serverURL + "crimbo11.php"
        self.requestData['pwd'] = session.pwd
        self.requestData['action'] = 'tradecandy'
        self.requestData['whichitem'] = itemId
        self.requestData['howmany'] = quantity
    
    def parseResponse(self):
        notCandyPattern = PatternManager.getOrCompilePattern('crimboItemIsNotCandy')
        if notCandyPattern.search(self.responseText):
            raise Error.Error("That item is not candy.", Error.WRONG_KIND_OF_ITEM)
        
        notEnoughCandyPattern = PatternManager.getOrCompilePattern('crimboNotEnoughCandy')
        if notEnoughCandyPattern.search(self.responseText):
            raise Error.Error("You do not have enough of that candy.", Error.ITEM_NOT_FOUND)

        creditsReceivedPattern = PatternManager.getOrCompilePattern('crimboCandyCreditsReceived')
        match = creditsReceivedPattern.search(self.responseText)
        if match:
            credits = int(match.group(1).replace(',', ''))
            self.responseData["credits"] = credits
        else:
            raise Error.Error("Unknown response.", Error.REQUEST_FATAL)
