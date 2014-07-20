from kol.request.GenericAdventuringRequest import GenericAdventuringRequest

class AdventureRequest(GenericAdventuringRequest):
    "A request used to initiate an adventure at any location."

    def __init__(self, session, locationId):
        super(AdventureRequest, self).__init__(session)
        self.url = session.serverURL + "adventure.php"
        self.requestData['snarfblat'] = locationId
