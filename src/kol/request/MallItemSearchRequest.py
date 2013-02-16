import kol.Error as Error
from GenericRequest import GenericRequest
from kol.database import ItemDatabase
from kol.manager import PatternManager
from kol.util import Report

class MallItemSearchRequest(GenericRequest):
    """
    Searches for an item at the mall.
    """

    CATEGORY_ALL = 'allitems'
    CATEGORY_FOOD = 'food'
    CATEGORY_BOOZE = 'booze'
    CATEGORY_OTHER_CONSUMABLES = 'othercon'
    CATEGORY_WEAPONS = 'weapons'
    CATEGORY_HATS = 'hats'
    CATEGORY_SHIRTS = 'shirts'
    CATEGORY_PANTS = 'pants'
    CATEGORY_ACCESSORIES = 'acc'
    CATEGORY_OFF_HAND = 'offhand'
    CATEGORY_FAMILIAR_EQUIPMENT = 'famequip'
    CATEGORY_COMBAT_ITEMS = 'combat'
    CATEGORY_POTIONS = 'potions'
    CATEGORY_HP_RESTORERS = 'hprestore'
    CATEGORY_MP_RESTORERS = 'mprestore'
    CATEGORY_FAMILIARS = 'familiars'

    def __init__(self, session, searchQuery, category=CATEGORY_ALL, noLimits=False, maxPrice=0, numResults=0):
        super(MallItemSearchRequest, self).__init__(session)
        self.url = session.serverURL + 'mall.php'
        self.requestData['didadv'] = 1
        self.requestData['pudnuggler'] = searchQuery
        self.requestData['category'] = category
        self.requestData['justitems'] = '0'
        self.requestData['sortresultsby'] = 'price'
        self.requestData['max_price'] = maxPrice
        self.requestData['x_cheapest'] = numResults
        if noLimits:
            self.requestData['nolimits'] = '1'
        else:
            self.requestData['nolimits'] = '0'

    def parseResponse(self):
        items = []
        itemMatchPattern = PatternManager.getOrCompilePattern('mallItemSearchResult')
        itemDetailsPattern = PatternManager.getOrCompilePattern('mallItemSearchDetails')
        for itemMatch in itemMatchPattern.finditer(self.responseText):
            matchText = itemMatch.group(1)
            match = itemDetailsPattern.search(matchText)
            itemId = int(match.group('itemId'))
            try:
                item = ItemDatabase.getItemFromId(itemId)
                item["price"] = int(match.group('price').replace(',', ''))
                item["storeId"] = int(match.group('storeId'))
                item["storeName"] = match.group('storeName').replace('<br>', ' ')
                item["quantity"] = int(match.group('quantity').replace(',', ''))
                limit = match.group('limit').replace(',', '')
                if len(limit) > 0:
                    limit = int(limit)
                    item["limit"] = limit
                if matchText.find('limited"') >= 0:
                    item["hitLimit"] = True
                items.append(item)
            except Error.Error, inst:
                if inst.code == Error.ITEM_NOT_FOUND:
                    Report.info("itemdatabase", "Unrecognized item found in mall search: %s" % itemId, inst)
                else:
                    raise inst

        self.responseData["results"] = items
