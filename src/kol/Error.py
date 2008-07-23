class Error(Exception):
	"Base class for KoL Exceptions."
	def __init__(self, message):
		self.message = message
	
	def __str__(self):
		return self.message

class IncorrectPasswordError(Error):
	"An exception raised when a user tries to login with a bad password."
	def __init__(self, message):
		self.message = message

class ItemNotFoundError(Error):
	"An exception raised when an item can not be found."
	def __init__(self, message):
		self.message = message

class LoginError(Error):
	"An exception raised during login."
	def __init__(self, message, timeToWait=60):
		self.message = message
		self.timeToWait = timeToWait

class NightlyMaintenanceError(Error):
	"An exception raised when Nightly Maintenance is occurring."
	def __init__(self, message):
		self.message = message

class NotEnoughItemsError(Error):
	"An exception raised when the user tries to perform an action on an item they don't have enough of."
	def __init__(self, message):
		self.message = message

class NotLoggedInError(Error):
	"An exception raised if the session thinks it is logged in when in reality it isn't."
	def __init__(self, message):
		self.message = message

class ParseMessageError(Error):
	"An exception used by bots raised when a kmail message can not be understood correctly."

class RequestError(Error):
	"An exception raised during requests."
	def __init__(self, message):
		self.message = message

class SkillNotFoundError(Error):
	"An exception raised when a skill could not be found."
	def __init__(self, message):
		self.message = message

class UnableToPulverizeItemError(Error):
	"An exception raised when a user tried to pulverize an item that can not be pulverized."
	def __init__(self, message):
		self.message = message

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
