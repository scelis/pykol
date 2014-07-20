import kol.Error as Error
from GenericRequest import GenericRequest
from kol.manager import PatternManager

class AutoSellRequest(GenericRequest):
    "Sells items via the autosell system"

    ALL = 1
    ALL_BUT_ONE = 2
    QUANTITY = 3

    def __init__(self, session, itemList, howMany, amount=1):
        super(AutoSellRequest, self).__init__(session)
        self.url = session.serverURL + "sellstuff_ugly.php"
        self.requestData["pwd"] = session.pwd
        self.requestData["action"] = "sell"

        if howMany == self.ALL:
            self.requestData["mode"] = self.ALL
        elif howMany == self.ALL_BUT_ONE:
            self.requestData["mode"] = self.ALL_BUT_ONE
        elif howMany == self.QUANTITY:
            self.requestData["mode"] = self.QUANTITY
            self.requestData["quantity"] = amount
        else:
            raise Error.Error("Invalid AutoSell Mode Selected.", Error.REQUEST_GENERIC)

        for item in itemList:
            self.requestData[("item"+str(item["id"]))] = str(item["id"])

    def parseResponse(self):
        salePattern = PatternManager.getOrCompilePattern("autosellResponse")

        saleMatch = salePattern.search(self.responseText)
        if saleMatch:
            multiItemPattern = PatternManager.getOrCompilePattern("autosellItems")
            finalTwoPattern = PatternManager.getOrCompilePattern("autosellLastTwo")
            finalOnePattern = PatternManager.getOrCompilePattern("autosellOne")

            salesTotal = int(saleMatch.group(2).replace(',',''))

            soldItems = []
            lastItemIndex = None
            for itemMatch in multiItemPattern.finditer(saleMatch.group(1)):
                # We cannot look up the item because the names are likely pluralized
                name = itemMatch.group(2)
                if itemMatch.group(1) == "":
                    quantity = 1
                else:
                    quantity = int(itemMatch.group(1).replace(',',''))

                soldItems.append({"quantity":quantity, "name":name})
                lastItemIndex = itemMatch.end(2)

            if lastItemIndex != None:
                finalMatch = finalTwoPattern.search(saleMatch.group(1)[lastItemIndex+1:])
            else:
                finalMatch = finalTwoPattern.search(saleMatch.group(1))

            if finalMatch:
                if finalMatch.group(2) != "":
                    name = finalMatch.group(2)
                    if finalMatch.group(1) == "":
                        quantity = 1
                    else:
                        quantity = int(finalMatch.group(1).replace(',',''))
                    soldItems.append({"quantity":quantity, "name":name})

                name = finalMatch.group(4)
                if finalMatch.group(3) == "":
                    quantity = 1
                else:
                    quantity = int(finalMatch.group(3).replace(',',''))
                soldItems.append({"quantity":quantity, "name":name})
            else:
                singleItem = finalOnePattern.search(saleMatch.group(1))
                name = singleItem.group(2)
                if singleItem.group(1) == "":
                    quantity = 1
                else:
                    quantity = int(singleItem.group(1).replace(',',''))
                soldItems.append({"quantity":quantity, "name":name})
        else:
            salesTotal = 0
            soldItems = []

        self.responseData["meatGained"] = salesTotal
        self.responseData["itemsSold"] = soldItems
