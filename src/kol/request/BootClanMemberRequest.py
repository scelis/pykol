from GenericRequest import GenericRequest

class BootClanMemberRequest(GenericRequest):
    def __init__(self, session, userId):
        super(BootClanMemberRequest, self).__init__(session)
        self.url = session.serverURL + "clan_members.php"
        self.requestData['pwd'] = session.pwd
        self.requestData['action'] = 'modify'
        self.requestData['begin'] = '1'
        self.requestData['pids[]'] = userId
        self.requestData['boot%s' % userId] = 'on'
