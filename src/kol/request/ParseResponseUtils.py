from kol.database import ItemDatabase
from kol.manager import PatternManager

def parseItemsReceived(text):
	items = []
	
	singleItemPattern = PatternManager.getOrCompilePattern('acquireSingleItem')
	for match in singleItemPattern.finditer(text):
		descId = int(match.group(1))
		item = ItemDatabase.getItemFromDescId(descId, self.session)
		item["quantity"] = 1
		items.append(item)
	
	multiItemPattern = PatternManager.getOrCompilePattern('acquireMultipleItems')
	for match in multiItemPattern.finditer(text):
		descId = int(match.group(1))
		quantity = int(match.group(2).replace(',', ''))
		item = ItemDatabase.getItemFromDescId(descId, self.session)
		item["quantity"] = quantity
		items.append(item)	
	
	return items

def parseMeatReceived(text):
	meatPattern = PatternManager.getOrCompilePattern('gainMeat')
	match = meatPattern.search(self.responseText)
	if match:
		return int(match.group(1).replace(',', ''))
	return 0

def parseSubstatsGained(text, checkMuscle=True, checkMysticality=True, checkMoxie=True):
	substats = {}
	
	if checkMuscle:
		muscPattern = PatternManager.getOrCompilePattern('muscleGainLoss')
		muscMatch = muscPattern.search(text)
		if muscMatch:
			muscle = int(muscMatch.group(2).replace(',', ''))
			if muscMatch.group(1) == "gain":
				substats["muscle"] = muscle
			else:
				substats["muscle"] = -1 * muscle
				
	if checkMysticality:
		mystPattern = PatternManager.getOrCompilePattern('mysticalityGainLoss')
		mystMatch = mystPattern.search(text)
		if mystMatch:
			myst = int(mystMatch.group(2).replace(',', ''))
			if mystMatch.group(1) == "gain":
				substats["mysticality"] = myst
			else:
				substats["mysticality"] = -1 * myst
				
	if checkMoxie:
		moxPattern = PatternManager.getOrCompilePattern('moxieGainLoss')
		moxMatch = moxPattern.search(text)
		if moxMatch:
			moxie = int(moxMatch.group(2).replace(',', ''))
			if moxMatch.group(1) == "gain":
				substats["moxie"] = moxie
			else:
				substats["moxie"] = -1 * moxie
				
	return substats
