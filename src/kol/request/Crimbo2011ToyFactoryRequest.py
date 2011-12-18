import kol.Error as Error
from GenericRequest import GenericRequest
from kol.manager import PatternManager

class Crimbo2011ToyFactoryRequest(GenericRequest):
    def __init__(self, session, itemId, quantity, targetPlayer='', note=''):
        super(Crimbo2011ToyFactoryRequest, self).__init__(session)
        self.url = session.serverURL + "crimbo11.php"
        self.requestData['pwd'] = session.pwd
        self.requestData['action'] = 'reallybuygifts'
        self.requestData['whichitem'] = itemId
        self.requestData['howmany'] = quantity
        self.requestData['towho'] = targetPlayer
        self.requestData['note'] = note
    
    def parseResponse(self):
        invalidGiftPattern = PatternManager.getOrCompilePattern('crimboInvalidGift')
        if invalidGiftPattern.search(self.responseText):
            raise Error.Error("Invalid gift selected.", Error.WRONG_KIND_OF_ITEM)
        
        invalidPlayerPattern = PatternManager.getOrCompilePattern('crimboInvalidPlayer')
        if invalidPlayerPattern.search(self.responseText):
            raise Error.Error("Invalid player.", Error.USER_NOT_FOUND)
        
        giftAlreadyReceivedPattern = PatternManager.getOrCompilePattern('crimboUserAlreadyReceivedGift')
        if giftAlreadyReceivedPattern.search(self.responseText):
            raise Error.Error("That player has already received that gift.", Error.ALREADY_COMPLETED)
