from GenericAdventuringRequest import GenericAdventuringRequest

class CombatRequest(GenericAdventuringRequest):
	"""
	A request used for a single round of combat. The user may attack, use an item or skill, or
	attempt to run away.
	"""
	
	# What follows are a list of available actions.
	ATTACK = 0
	USE_ITEM = 1
	USE_SKILL = 2
	RUN_AWAY = 3
	
	def __init__(self, session, action, param=None):
		"""
		In this constructor, action should be set to CombatRequest.ATTACK, CombatRequest.USE_ITEM,
		CombatRequest.USE_SKILL, or CombatRequest.RUN_AWAY. If a skill or item is to be used, the
		caller should also specify param to be the number of the item or skill the user wishes
		to use.
		"""
		super(CombatRequest, self).__init__(session)
		self.url = session.serverURL + "fight.php"
		
		if action == ATTACK:
			self.requestData["action"] = "attack"
		elif action == USE_ITEM:
			self.requestData["action"] = "useitem"
			self.requestData["whichitem"] = param
		elif action == USE_SKILL:
			self.requestData["action"] = "skill"
			self.requestData["whichskill"] = param
		elif action == RUN_AWAY:
			self.requestData["action"] = "runaway"
