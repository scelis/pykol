from kol.request.GenericRequest import GenericRequest

class CampgroundRestRequest(GenericRequest):
    "Rests at the user's campground."

    def __init__(self, session):
        super(CampgroundRestRequest, self).__init__(session)
        self.url = session.serverURL + 'campground.php?action=rest'
