from GenericRequest import GenericRequest
from kol.Error import InvalidActionError, UserShouldNotBeHereError
from kol.manager import PatternManager
from kol.request import ParseResponseUtils

class GenericAdventuringRequest(GenericRequest):
	"""
	A base class used for common adventuring functionality. Other request classes related to
	adventuring should probably extend this one.
	"""
	
	def parseResponse(self):
		shouldNotBeHerePattern = PatternManager.getOrCompilePattern('userShouldNotBeHere')
		if shouldNotBeHerePattern.search(self.responseText)
			raise UserShouldNotBeHereError("Unable to adventure. You should not be here.")
		
		url = self.response.geturl()
		if url.find("/fight.php") >= 0:
			# See if the user tried to perform an invalid action.
			twiddlingThumbsPattern = PatternManager.getOrCompilePattern('twiddlingThumbs')
			if twiddlingThumbs.search(self.responseText)
				raise InvalidActionError("Could not perform action. Thumbs were twiddled.")
			
			# Get the monster's name.
			self.responseData["adventureType"] = "combat"
			monsterNamePattern = PatternManager.getOrCompilePattern('monsterName')
			monsterNameMatch = monsterNamePattern.search(self.responseText)
			self.responseData["monsterName"] = monsterNameMatch.group(1)
			
			# Check to see if the fight was won or lost.
			fightWonPattern = PatternManager.getOrCompilePattern('fightWon')
			if fightWonPattern.search(self.responseText):
				self.responseData["fightWon"] = True
			else:
				fightLostPattern = PatternManager.getOrCompilePattern('fightLost')
				if fightLostPattern.search(self.responseText):
					self.responseData["fightLost"] = True
			
			# Get items, meat, and substats gained. We always need to check these since they can
			# happen at any point during the fight.
			self.responseData["items"] = ParseResponseUtils.parseItemsReceived(self.responseText)
			self.responseData["meat"] = ParseResponseUtils.parseMeatReceived(self.responseText)
			self.responseData["substats"] = ParseResponseUtils.parseSubstatsGained(self.responseText)
			
		elif url.find("/choice.php") >= 0:
			self.responseData["adventureType"] = "choice"
			choiceIdentifierPattern = PatternManager.getOrCompilePattern('choiceIdentifier')
			choiceIdentifierMatch = choiceIdentifierPattern.search(self.responseText)
			if choiceIdentifierMatch:
				choiceNamePattern = PatternManager.getOrCompilePattern('choiceName')
				self.responseData["choiceId"] = choiceIdentifierMatch.group(1)
				self.responseData["choiceName"] = choiceNamePattern.search(self.responseText).group(1)
			else:
				self.responseData["items"] = ParseResponseUtils.parseItemsReceived(self.responseText)
				self.responseData["meat"] = ParseResponseUtils.parseMeatReceived(self.responseText)
				self.responseData["substats"] = ParseResponseUtils.parseSubstatsGained(self.responseText)
				
		elif url.find("/adventure.php") >= 0:
			self.responseData["adventureType"] = "noncombat"
			noncombatNamePattern = PatternManager.getOrCompilePattern('noncombatName')
			noncombatNameMatch = noncombatNamePattern.search(self.responseText)
			if noncombatNameMatch:
				self.responseData["noncombatName"] = noncombatNameMatch.group(1)
			self.responseData["items"] = ParseResponseUtils.parseItemsReceived(self.responseText)
			self.responseData["meat"] = ParseResponseUtils.parseMeatReceived(self.responseText)
			self.responseData["substats"] = ParseResponseUtils.parseSubstatsGained(self.responseText)
		else:
			raise RequestError("Adventure URL not recognized: %s" % url)
