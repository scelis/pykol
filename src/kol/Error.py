__i = 0
LOGIN_FAILED_GENERIC = __i; __i += 1
LOGIN_FAILED_BAD_PASSWORD = __i; __i += 1
NIGHTLY_MAINTENANCE = __i; __i += 1
NOT_LOGGED_IN = __i; __i += 1
REQUEST_GENERIC = __i; __i += 1
REQUEST_FATAL = __i; __i += 1
INVALID_ACTION = __i; __i += 1
INVALID_ITEM = __i; __i += 1
INVALID_LOCATION = __i; __i += 1
INVALID_USER = __i; __i += 1
ITEM_NOT_FOUND = __i; __i += 1
SKILL_NOT_FOUND = __i; __i += 1
EFFECT_NOT_FOUND = __i; __i += 1
RECIPE_NOT_FOUND = __i; __i += 1
WRONG_KIND_OF_ITEM = __i; __i += 1
USER_IN_HARDCORE_RONIN = __i; __i += 1
USER_IS_IGNORING = __i; __i += 1
USER_IS_DRUNK = __i; __i += 1
USER_IS_FULL = __i; __i += 1
USER_IS_LOW_LEVEL = __i; __i += 1
USER_IS_WRONG_PROFESSION = __i; __i += 1
USER_NOT_FOUND = __i; __i += 1
NOT_ENOUGH_ADVENTURES = __i; __i += 1
NOT_ENOUGH_MEAT = __i; __i += 1
LIMIT_REACHED = __i; __i += 1
ALREADY_COMPLETED = __i; __i += 1
BOT_REQUEST = __i; __i += 1

class Error(Exception):
    def __init__(self, msg, code=-1):
        self.msg = msg
        self.code = code

    def __str__(self):
        return self.msg
