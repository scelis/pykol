from GenericRequest import GenericRequest

class ToggleAcceptingClanApplicationsRequest(GenericRequest):
    "Toggle whether or not the clan accepts new applications."

    def __init__(self, session):
        super(ToggleAcceptingClanApplicationsRequest, self).__init__(session)
        self.url = session.serverURL + "clan_admin.php?action=noapp"
