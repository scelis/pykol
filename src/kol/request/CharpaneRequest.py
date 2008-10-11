from GenericRequest import GenericRequest
from kol.manager import PatternManager

class CharpaneRequest(GenericRequest):
	"Requests the user's character pane."
	
	def __init__(self, session):
		super(CharpaneRequest, self).__init__(session)
		self.url = session.serverURL + 'charpane.php'

	def parseResponse(self):
		characterLevelPattern = PatternManager.getOrCompilePattern('characterLevel')		
		match = characterLevelPattern.search(self.responseText)
		if match:
			self.responseData["level"] = int(match.group(1))
			self.responseData["levelTitle"] = str(match.group(2))
		
		characterHPPattern = PatternManager.getOrCompilePattern('characterHP')
		match = characterHPPattern.search(self.responseText)
		if match:
			self.responseData["currentHP"] = int(match.group(1))
			self.responseData["maxHP"] = int(match.group(2))
		
		characterMPPattern = PatternManager.getOrCompilePattern('characterMP')
		match = characterMPPattern.search(self.responseText)
		if match:
			self.responseData["currentMP"] = int(match.group(1))
			self.responseData["maxMP"] = int(match.group(2))
		
		characterMeatPattern = PatternManager.getOrCompilePattern('characterMeat')
		match = characterMeatPattern.search(self.responseText)
		if match:
			self.responseData["meat"] = int(match.group(1).replace(',', ''))
		
		characterAdventuresPattern = PatternManager.getOrCompilePattern('characterAdventures')
		match = characterAdventuresPattern.search(self.responseText)
		if match:
			self.responseData["adventures"] = int(match.group(1))
		
		currentFamiliarPattern = PatternManager.getOrCompilePattern('currentFamiliar')
		match = currentFamiliarPattern.search(self.responseText)
		if match:
			self.responseData["familiar"] = {'name':str(match.group(1)), 'type':str(match.group(3)), 'weight':int(match.group(2))}
		
		effects = []
		characterEffectPattern = PatternManager.getOrCompilePattern('characterEffect')
		for match in characterEffectPattern.finditer(self.responseText):
			effect = {}
			effect["name"] = str(match.group(1))
			effect["turns"] = int(match.group(2))
			effects.append(effect)
		if len(effects) > 0:
			self.responseData["effects"] = effects
			
		characterMusclePattern = PatternManager.getOrCompilePattern('characterMuscle')
		match = characterMusclePattern.search(self.responseText)
		if match:
			if match.group(1) and len(str(match.group(1))) > 0:
				self.responseData["buffedMuscle"] = int(match.group(1))
			self.responseData["baseMuscle"] = int(match.group(2))
			
		characterMoxiePattern = PatternManager.getOrCompilePattern('characterMoxie')
		match = characterMoxiePattern.search(self.responseText)
		if match:
			if match.group(1) and len(str(match.group(1))) > 0:
				self.responseData["buffedMoxie"] = int(match.group(1))
			self.responseData["baseMoxie"] = int(match.group(2))
			
		characterMysticalityPattern = PatternManager.getOrCompilePattern('characterMysticality')
		match = characterMysticalityPattern.search(self.responseText)
		if match:
			if match.group(1) and len(str(match.group(1))) > 0:
				self.responseData["buffedMysticality"] = int(match.group(1))
			self.responseData["baseMysticality"] = int(match.group(2))

		characterRoninPattern = PatternManager.getOrCompilePattern('characterRonin')
		match = characterRoninPattern.search(self.responseText)
		if match:
			self.responseData["roninLeft"] = int(match.group(1))

		characterMindControlPattern = PatternManager.getOrCompilePattern('characterMindControl')
		match = characterMindControlPattern.search(self.responseText)
		if match:
			self.responseData["mindControl"] = int(match.group(1))
