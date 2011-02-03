from GenericRequest import GenericRequest

class PutItemInStoreRequest(GenericRequest):
    "Adds items to your mall store."

    def __init__(self, session, items):
        super(PutItemInStoreRequest, self).__init__(session)
        self.url = session.serverURL + 'managestore.php'
        self.requestData['action'] = "additem"
        self.requestData['pwd'] = session.pwd

        ctr = 1
        for item in items:
            self.requestData['item%s' % ctr] = item["id"]
            if "price" in item:
                self.requestData['price%s' % ctr] = item["price"]
            else:
                self.requestData['price%s' % ctr] = "999999999"
            if "limit" in item:
                self.requestData['limit%s' % ctr] = item["limit"]
            else:
                self.requestData['limit%s' % ctr] = ""
            if "quantity" in item:
                self.requestData['qty%s' % ctr] = item["quantity"]
            else:
                self.requestData['qty%s' % ctr] = "1"
            ctr += 1

    def parseResponse(self):
        # TODO: Determine which items were added successfully and which were not.
        pass
