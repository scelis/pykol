from kol.request.GenericRequest import GenericRequest
from kol.database import ItemDatabase
from kol.manager import PatternManager

"""
Needed:  Someone who has access to the various stat-boosting clan equipment
(Tan-U-Lots, Hobo-Flex, Arcane Tomes and Whatnot) should check
whether a single mouse click is sufficient to use the furniture, or
if it will be neccessary to code forms similar to what has been done for
the clan sofa.

Additionally, a test that involves stat gain of some kind, for the same reasons
as above.
"""

"""
This is the furniture that I know about/ have checked myself:
A Hanging Meat Orchid :: spot 1, furniture 4
A Shelf of Self-Help Books :: spot 2, furniture 3
Mr. Klaw Skill Game :: spot 3, furniture 3
A Potted Meat Bush :: stop 4, furniture 2
A Comfy Sofa :: spot 5, furniture 3 --Remember to include # of turns in argument
A Potted Meat Tree :: spot 9, furniture 3

The remainder I've guessed from image files names from the KOL wiki:
Girls of Loathing Calendar :: spot 1, furniture 1
Boys of Loathing Calendar :: spot 1, furniture 2
An Infuriating Painting :: spot 1, furniture 3

A Shelf Full of Arcane Tomes and Whatnot :: spot 2, furniture 1
A Shelf Full of Sports Memorabilia :: spot 2, furniture 2

A Soda Machine :: spot 3, furniture 1
A Jukebox :: spot 3, furniture 2

An Old-Timey Radio :: spot 4, furniture 1
An Inspirational Desk Calendar :: spot 4, furniture 3

A Wrestling Mat :: spot 5, furniture 1
Tan-U-Lots Tanning Bed :: spot 5, furniture 2

Hobo-Flex Workout System :: spot 9, furniture 1
A Snack Machine :: spot 9, furniture 2
"""

class RumpusRequest(GenericRequest):
	"Allows interactions with furniture in the rumpus room"
	def __init__(self, session, spot, furni, numturns=1):
		super(RumpusRequest, self).__init__(session)
		# Handle clan sofa requests differently than others
		if spot == 5 and furni == 3:
			self.url = session.serverURL + "clan_rumpus.php"
			self.requestData['preaction'] = "nap"
			self.requestData['numturns'] = numturns
		else:
			self.url = session.serverURL + 'clan_rumpus.php?action=click&spot=' + str(spot) + '&furni=' + str(furni)

	
	def parseResponse(self):
		singleItemPattern = PatternManager.getOrCompilePattern('acquireSingleItem')
		multiItemPattern = PatternManager.getOrCompilePattern('acquireMultipleItems')
		meatPattern = PatternManager.getOrCompilePattern('gainMeat')
		statGainPattern = PatternManager.getOrCompilePattern('statGain')
		statLossPattern = PatternManager.getOrCompilePattern('statLoss')
		hpGainPattern = PatternManager.getOrCompilePattern('hpGain')
		hpLossPattern = PatternManager.getOrCompilePattern('hpLoss')
		mpGainPattern = PatternManager.getOrCompilePattern('mpGain')
		mpLossPattern = PatternManager.getOrCompilePattern('mpLoss')
		
		response = {}
		
		# Find items recieved, if any.
		items = []
		for match in singleItemPattern.finditer(self.responseText):
			descId = int(match.group(1))
			item = ItemDatabase.getItemFromDescId(descId, self.session)
			item["quantity"] = 1
			items.append(item)
		for match in multiItemPattern.finditer(self.responseText):
			descId = int(match.group(1))
			quantity = int(match.group(2).replace(',', ''))
			item = ItemDatabase.getItemFromDescId(descId, self.session)
			item["quantity"] = quantity
			items.append(item)
		if len(items) > 0:
			response["item"] = items

		# Find how much meat was attached to the message.
		meat = 0
		meatMatch = meatPattern.search(self.responseText)
		if meatMatch:
			meat = int(meatMatch.group(1).replace(',', ''))
		if meat > 0:
			response["meat"] = meat
			
		# Check for stat gain/loss
		stats = {}
		for match in statGainPattern.finditer(self.responseText):
			substat = str(match.group(2))
			points = int(match.group(1))
			stats[substat] = points
		if len(stats) > 0:
			response["statGain"] = stats
		stats = {}
		for match in statLossPattern.finditer(self.responseText):
			substat = str(match.group(2))
			points = int(match.group(1))
			stats[substat] = points
		if len(stats) > 0:
			response["statLoss"] = stats
			
		# Check for HP and MP gain/loss
		match = hpGainPattern.search(self.responseText)
		if match:
			hp = int(match.group(1))
			response["hpGain"] = hp
		match = hpLossPattern.search(self.responseText)
		if match:
			hp = int(match.group(1))
			response["hpLoss"] = hp
		match = mpGainPattern.search(self.responseText)
		if match:
			mp = int(match.group(1))
			response["mpGain"] = mp
		match = mpLossPattern.search(self.responseText)
		if match:
			mp = int(match.group(1))
			response["mpLoss"] = mp

		self.responseData = response