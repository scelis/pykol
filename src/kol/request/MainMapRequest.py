from GenericRequest import GenericRequest

class MainMapRequest(GenericRequest):
    def __init__(self, session):
        super(MainMapRequest, self).__init__(session)
        self.url = session.serverURL + "main.php"
