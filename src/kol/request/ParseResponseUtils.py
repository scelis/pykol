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
	meatPattern = PatternManager.getOrCompilePattern('loseMeat')
	match = meatPattern.search(self.responseText)
	if match:
		return -1 * int(match.group(1).replace(',', ''))	
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

def parseStatPointsGained(text, checkMuscle=True, checkMysticality=True, checkMoxie=True):
	statPoints = {}
	
	if checkMuscle:
		muscPattern = PatternManager.getOrCompilePattern('musclePointGainLoss')
		muscMatch = muscPattern.search(text)
		if muscMatch:
			if muscMatch.group(1) == "gain":
				statPoints["muscle"] = '+'
			else:
				statPoints["muscle"] = '-'
				
	if checkMysticality:
		mystPattern = PatternManager.getOrCompilePattern('mystPointGainLoss')
		mystMatch = mystPattern.search(text)
		if mystMatch:
			if mystMatch.group(1) == "gain":
				statPoints["mysticality"] = '+'
			else:
				statPoints["mysticality"] = '-'
				
	if checkMoxie:
		moxPattern = PatternManager.getOrCompilePattern('moxiePointGainLoss')
		moxMatch = moxPattern.search(text)
		if moxMatch:
			if moxMatch.group(1) == "gain":
				statPoints["moxie"] = '+'
			else:
				statPoints["moxie"] = '-'
				
	return statPoints

def parseLevelGained(text):
	level = {}
	
	levelPattern = PatternManager.getOrCompilePattern('')
	levelMatch = levelPattern.search(text)
	if levelMatch:
		level["level"] = '+'
	
	return level

def parseHPGained(text):
	hpPattern = PatternManager.getOrCompilePattern('hpGainLoss')
	# Need to do an iteration because it may happen multiple times in combat
	# e.g. Items use to gain, then monster attack for loss
	hp = 0
	for hpMatch in hpPattern.finditer(text)
		hpChange = int(hpMatch.group(2).replace(',', ''))
		if hpMatch.group(1) == "gain":
			hp = hp + hpChange
		else:
			hp = hp - hpChange
	
	return hp

def parseMPGained(text):
	mpPattern = PatternManager.getOrCompilePattern('mpGainLoss')
	# Need to do an iteration because it may happen multiple times in combat
	mp = 0
	for mpMatch in mpPattern.finditer(text)
		mpChange = int(mpMatch.group(2).replace(',', ''))
		if mpMatch.group(1) == "gain":
			mp = mp + mpChange
		else:
			mp = mp - mpChange
	
	return mp

def parseDrunkGained(text):
	drunk = 0
	drunkPattern = PatternManager.getOrCompilePattern('gainDrunk')
	match = drunkPattern.search(text)
	if match:
		drunk = int(match.group(1).replace(',',''))
	
	return drunk

def parseAdventureGained(text):
	adventures = 0
	adventurePattern = PatternManager.getOrCompilePattern('gainAdventures')
	match = adventurePattern.search(text)
	if match:
		adventures = int(match.group(1).replace(',',''))
	
	return adventures

def parseEffectsGained(text):
	effects = []
	effectPattern = PatternManager.getOrCompilePattern('gainEffect')
	for match in effectPattern.finditer(text):
		eff = {}
		eff["name"] = match.group(1)
		eff["turns"] = int(match.group(2).replace(',',''))
		effects.append(eff)
	
	return effects
