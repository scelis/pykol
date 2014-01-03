from kol.request.GenericRequest import GenericRequest
from kol.manager import PatternManager
import kol.Error as Error
from kol.util import Report

class RespondToTradeRequest(GenericRequest):
    
    def __init__(self, session, tradeid, items=None, meat=0, message=""):
        super(RespondToTradeRequest, self).__super__(session)
        self.url = session.serverURL + "makeoffer.php"
        self.requestData['action'] = 'counter'
        self.requestData['pwd'] = session.pwd
        self.requestData['whichoffer'] = tradeid
        self.requestData['offermeat'] = meat
        self.requestData['memo2'] = message
        ctr = 1
        for item in items:
            self.requestData['whichitem' + str(ctr)] = item['itemID']
            self.requestData['howmany' + str(ctr)] = item['quantity']
            ctr += 1
    
    def parseResponse(self):
        noMeatPattern = PatternManager.getOrCompilePattern('traderHasNotEnoughMeat')
        if noMeatPattern.search(self.responseText):
            raise Error.Error("You don't have as much meat as you're promising.", Error.NOT_ENOUGH_MEAT)
        
        noItemsPattern = PatternManager.getOrCompilePattern('traderHasNotEnoughItems')
        if noItemsPattern.search(self.responseText):
            raise Error.Error("You don't have as many items as you're promising.", Error.NOT_ENOUGH_ITEMS)
        
        #Not testing for an offer being cancelled due to a bug in KoL - space reserved
        
        successPattern = PatternManager.getOrCompilePattern('tradeResponseSentSuccessfully')
        if successPattern.search(self.responseText):
            Report.trace("request", "Response to trade " + str(self.requestData['whichoffer']) + ' sent successfully.')
        else:
            raise Error.Error("Unknown error sending response to trade " + str(self.requestData['whichoffer']), Error.REQUEST_GENERIC)