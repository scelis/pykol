from kol.request.GenericRequest import GenericRequest
from kol.manager import PatternManager

class RumpusRoomRequest(GenericRequest):
	"Determines what furniture is present in the rumpus room"
	def __init__(self, session):
		super(RumpusRoomRequest, self).__init__(session)
		self.url = session.serverURL + 'clan_rumpus.php'
		
	def parseResponse(self):
		clanFurniture = []
		
		# Load Patterns
		girlsCalendarPattern = PatternManager.getOrCompilePattern('girlsCalendar')
		match = girlsCalendarPattern.search(self.responseText)
		if match:
			clanFurniture.append("Girls of Loathing Calendar")
			
		boysCalendarPattern = PatternManager.getOrCompilePattern('boysCalendar')
		match = boysCalendarPattern.search(self.responseText)
		if match:
			clanFurniture.append("Boys of Loathing Calendar")
			
		paintingPattern = PatternManager.getOrCompilePattern('infuriatingPainting')
		match = paintingPattern.search(self.responseText)
		if match:
			clanFurniture.append("An Infuriating Painting")
			
		orchidPattern = PatternManager.getOrCompilePattern('meatOrchid')
		match = orchidPattern.search(self.responseText)
		if match:
			clanFurniture.append("An Exotic Hanging Meat Orchid")
			
		tomesPattern = PatternManager.getOrCompilePattern('arcaneTomes')
		match = tomesPattern.search(self.responseText)
		if match:
			clanFurniture.append("A Collection of Arcane Tomes and Whatnot")
			
		sportsPattern = PatternManager.getOrCompilePattern('sportsMem')
		match = sportsPattern.search(self.responseText)
		if match:
			clanFurniture.append("A Collection of Sports Memorabilia")
			
		helpBooksPattern = PatternManager.getOrCompilePattern('selfHelp')
		match = helpBooksPattern.search(self.responseText)
		if match:
			clanFurniture.append("A Collection of Self-Help Books")
			
		sodaMachinePattern = PatternManager.getOrCompilePattern('sodaMachine')
		match = sodaMachinePattern.search(self.responseText)
		if match:
			clanFurniture.append("A Soda Machine")
			
		jukeboxPattern = PatternManager.getOrCompilePattern('jukebox')
		match = jukeboxPattern.search(self.responseText)
		if match:
			clanFurniture.append("A Jukebox")
			
		mrKlawPattern = PatternManager.getOrCompilePattern('mrKlaw')
		match = mrKlawPattern.search(self.responseText)
		if match:
			clanFurniture.append('A Mr. Klaw "Skill" Crane Game')
			
		radioPattern = PatternManager.getOrCompilePattern('oldRadio')
		match = radioPattern.search(self.responseText)
		if match:
			clanFurniture.append("An Old-Timey Radio")
			
		bushPattern = PatternManager.getOrCompilePattern('meatBush')
		match = bushPattern.search(self.responseText)
		if match:
			clanFurniture.append("A Potted Meat Bush")
			
		deskCalendarPattern = PatternManager.getOrCompilePattern('deskCal')
		match = deskCalendarPattern.search(self.responseText)
		if match:
			clanFurniture.append("An Inspirational Desk Calendar")
			
		wrestlingPattern = PatternManager.getOrCompilePattern('wrestling')
		match = wrestlingPattern.search(self.responseText)
		if match:
			clanFurniture.append("A Wrestling Mat")
			
		tanULotsPattern = PatternManager.getOrCompilePattern('tanULots')
		match = tanULotsPattern.search(self.responseText)
		if match:
			clanFurniture.append("A Tan-U-Lots Tanning Bed")
			
		comfySofaPattern = PatternManager.getOrCompilePattern('comfySofa')
		match = comfySofaPattern.search(self.responseText)
		if match:
			clanFurniture.append("A Comfy Sofa")
			
		hoboFlexPattern = PatternManager.getOrCompilePattern('hoboFlex')
		match = hoboFlexPattern.search(self.responseText)
		if match:
			clanFurniture.append("A Hobo-Flex Workout System")
			
		snackMachinePattern = PatternManager.getOrCompilePattern('snackMachine')
		match = snackMachinePattern.search(self.responseText)
		if match:
			clanFurniture.append("A Snack Machine")
			
		treePattern = PatternManager.getOrCompilePattern('meatTree')
		match = treePattern.search(self.responseText)
		if match:
			clanFurniture.append("A Potted Meat Tree")
			
		
		# Return the list of furniture
		if len(clanFurniture) > 0:
			self.responseData = clanFurniture
		else:
			self.responseData = None