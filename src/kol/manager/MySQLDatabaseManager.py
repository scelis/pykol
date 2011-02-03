"""
This module makes it easy to connect, disconnect, or reconnect to MySQL
databases.
"""

import MySQLdb
import MySQLdb.cursors

__arguments = {}
__databases = {}

def getDatabase(dbIdentifier):
    return __databases[dbIdentifier]

def connect(dbIdentifier, **kwargs):
    if "cursorclass" not in kwargs:
        kwargs["cursorclass"] = MySQLdb.cursors.DictCursor
    __arguments[dbIdentifier] = kwargs
    __databases[dbIdentifier] = MySQLdb.connect(**__arguments[dbIdentifier])
    return __databases[dbIdentifier]

def reconnect(dbIdentifier):
    __databases[dbIdentifier] = MySQLdb.connect(**__arguments[dbIdentifier])
    return __databases[dbIdentifier]

def disconnect(dbIdentifier):
    try:
        __databases[dbIdentifier].close()
    except:
        pass
    __databases[dbIdentifier] = None
