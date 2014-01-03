import kol.Error as Error

from kol.request.GenericRequest import GenericRequest
from kol.manager import PatternManager
from kol.util import Report

class ProposeTradeRequest(GenericRequest):
    
    def __init__(self, session, towhom, items=None, meat=0, message=""):
        super(ProposeTradeRequest, self).__init__(session);
        self.url = session.serverURL + "makeoffer.php"
        self.requestData["pwd"] = session.pwd
        self.requestData["action"] = "proposeoffer"
        self.requestData["towho"] = towhom;
        self.requestData["offermeat"] = meat;
        self.requestData["memo"] = message;
        if (items != None):
            ctr = 1;
            for item in items:
                self.requestData["howmany" + str(ctr)] = item["quantity"]
                self.requestData["whichitem" + str(ctr)] = item["itemID"]
                ctr += 1
    
    def parseResponse(self):
        ignorePattern = PatternManager.getOrCompilePattern("traderIgnoringUs")
        if ignorePattern.search(self.responseText):
            raise Error.Error("That player has you on his/her ignore list.", Error.USER_IS_IGNORING)
        
        roninPattern = PatternManager.getOrCompilePattern("traderIsInRoninHC")
        if roninPattern.search(self.responseText):
            raise Error.Error("That player is in Ronin or HC and cannot receive trade offers.", Error.USER_IN_HARDCORE_RONIN)
        
        itemsPattern = PatternManager.getOrCompilePattern("traderHasNotEnoughItems")
        if itemsPattern.search(self.responseText):
            raise Error.Error("You don't have enough of one or more of the items you're trying to trade.", Error.NOT_ENOUGH_ITEMS)
        
        meatPattern = PatternManager.getOrCompilePattern("traderHasNotEnoughMeat")
        if meatPattern.search(self.responseText):
            raise Error.Error("You don't have as much meat as you're trying to trade.", Error.NOT_ENOUGH_MEAT)
        
        chatBannedPattern = PatternManager.getOrCompilePattern("traderBannedFromChat")
        if chatBannedPattern.search(self.responseText):
            raise Error.Error("You are banned from chat and consequently cannot trade.", Error.BANNED_FROM_CHAT)
        
        successPattern = PatternManager.getOrCompilePattern("tradeSentSuccessfully")
        if successPattern.search(self.responseText):
            Report.trace("request", "Trade offer sent successfully.")
        else:
            raise Error.Error("Other error sending trade offer.", Error.ERROR)