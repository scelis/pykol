from GenericRequest import GenericRequest

class DiscardItemRequest(GenericRequest):
    def __init__(self, session, itemId):
        super(DiscardItemRequest, self).__init__(session)
        self.url = session.serverURL + "inventory.php?pwd=" + session.pwd \
            + "&action=discard&whichitem=" + str(itemId)

