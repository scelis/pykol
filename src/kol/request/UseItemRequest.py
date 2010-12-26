from GenericRequest import GenericRequest

class UseItemRequest(GenericRequest):
    def __init__(self, session, itemId):
        super(UseItemRequest, self).__init__(session)
        self.url = session.serverURL + "inv_use.php?pwd=" + session.pwd + "&whichitem=" + str(itemId)
