class Error(Exception):
	"Base class for KoL Exceptions."
	def __init__(self, message):
		self.message = message
	
	def __str__(self):
		return self.message

################
# Login Errors #
################
class LoginError(Error):
	"A generic exception raised during login."
	def __init__(self, message, timeToWait=60):
		self.message = message
		self.timeToWait = timeToWait

class IncorrectPasswordError(Error):
	"An exception raised when a user tries to login with a bad password."
	def __init__(self, message):
		self.message = message

class NightlyMaintenanceError(Error):
	"An exception raised when Nightly Maintenance is occurring."
	def __init__(self, message):
		self.message = message

class NotLoggedInError(Error):
	"An exception raised if the session thinks it is logged in when in reality it isn't."
	def __init__(self, message):
		self.message = message

##################
# Generic Errors #
##################
class RequestError(Error):
	"An exception raised during requests."
	def __init__(self, message):
		self.message = message

###################
# Database Errors #
###################
class ItemNotFoundError(Error):
	"An exception raised when an item can not be found in the item database."
	def __init__(self, message):
		self.message = message

class SkillNotFoundError(Error):
	"An exception raised when a skill could not be found."
	def __init__(self, message):
		self.message = message

##############
# Bot Errors #
##############
class ParseMessageError(Error):
	"An exception used by bots raised when a kmail message can not be understood correctly."

#######################
# Item-Related Errors #
#######################
class NotEnoughItemsError(Error):
	"An exception raised when the user tries to perform an action on an item they don't have enough of."
	def __init__(self, message):
		self.message = message

class UnableToPulverizeItemError(Error):
	"An exception raised when a user tried to pulverize an item that can not be pulverized."
	def __init__(self, message):
		self.message = message

#######################
# User-Related Errors #
#######################
class UserInHardcoreRoninError(Error):
	"""
	An exception raised when an action can not be performed because either the current user or
	the target user is in hardcore or ronin.
	"""
	def __init__(self, message):
		self.message = message

class UserIsIgnoringError(Error):
	"An exception raised when the target user is ignoring the current user."
	def __init__(self, message):
		self.message = message

###############
# Misc Errors #
###############
class InvalidRecipeError(Error):
	"An exception raised when the user tries to construct something using an invalid recipe."
	def __init__(self, message):
		self.message = message

class SkillMissingError(Error):
	"An exception raised when the user fails to perform an action because they are missing a skill."
	def __init__(self, message):
		self.message = message

class NotEnoughAdventuresLeftError(Error):
	"""
	An exception raised then the user attempts to perform an action and they don't have enough
	adventures left to complete it.
	"""
	def __init__(self, message):
		self.message = message

class NotEnoughMeatError(Error):
	"""
	An exception raised when the user tries to do something without enought meat
	on hand to successfully perform the action.
	"""
	def __init__(self, message):
		self.message = message

class NotAStoreError(Error):
	"""
	An exception raised when the user tries to visit a store that doesn't exist
	"""
	def __init__(self, message):
		self.message = message