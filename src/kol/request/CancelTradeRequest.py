from kol.request.GenericRequest import GenericRequest

class CancelTradeRequest(GenericRequest):
    
    """
    Cancel a trade request.
    tradeid - the ID of the trade being cancelled
    tradetype - the type of the trade being cancelled according to the constants set in the GetPendingTradesRequest module
    """
    def __init__(self, session, tradeid, tradetype):
        super(CancelTradeRequest, self).__init__(session)
        self.url = session.serverURL + "makeoffer.php"
        self.requestData['pwd'] = session.pwd
        self.requestData['action'] = 'cancel2' if tradetype = 4 else 'cancel1'
        self.requestData['whichoffer'] = tradeid
    
    def parseResponse(self):
        pass
        