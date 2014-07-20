from kol.request.GenericRequest import GenericRequest
from kol.manager import PatternManager
from kol.util import Report
import kol.Error as Error

class DeclineTradeOfferRequest(GenericRequest):
    
    def __init__(self, session, tradeid):
        super(DeclineTradeOfferRequest, self).__init__(session)
        self.url = session.serverURL + "makeoffer.php"
        self.requestData['pwd'] = session.pwd
        self.requestData['action'] = 'decline'
        self.requestData['whichoffer'] = tradeid
    
    def parseResponse(self):
        successPattern = PatternManager.getOrCompilePattern('tradeCancelledSuccessfully')
        if successPattern.search(self.responseText):
            Report.trace('request', "Trade offer " + str(self.requestData['whichoffer']) + " cancelled successfully.")
        else:
            raise Error.Error("Unknown error declining trade offer for trade " + str(self.requestData['whichoffer']), Error.REQUEST_GENERIC)