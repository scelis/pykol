import os
import threading
import time
import traceback

FATAL = 100
ALERT = 200
ERROR = 300
WARNING = 400
INFO = 500
TRACE = 600
DEBUG = 700

activeSections = ["*"]
outputLevel = TRACE
logLevel = INFO
includeThreadName = False

__logDirectory = None
__logFileName = None
__logFile = None
__logCurrentDate = None

def setLogDirectory(directory):
	global __logDirectory, __logFile
	__logDirectory = directory
	if __logFile != None:
		__logFile.close()
		__logFile = None
		
	# If the directory doesn't exist, let's create it.
	if not os.path.exists(__logDirectory):
		os.mkdir(__logDirectory)

def setLogFileName(fileName):
	global __logFileName, __logFile
	__logFileName = fileName
	if __logFile != None:
		__logFile.close()
		__logFile = None

def report(section, level, message, exception=None):
	global __logFile, __logCurrentDate
	
	if section in activeSections or '*' in activeSections:
		if level <= outputLevel or level <= logLevel:
			dateTimeStr = time.strftime("%Y-%m-%d %H:%M:%S")
			
			# Create the full message string.
			if includeThreadName:
				threadName = threading.currentThread().getName()
				if threadName != "MainThread":
					fullMessage = "%s -- [%s] %s" % (dateTimeStr, threadName, message)
				else:
					fullMessage = "%s -- %s" % (dateTimeStr, message)
			else:
				fullMessage = "%s -- %s" % (dateTimeStr, message)
			
			if level <= outputLevel:
				print fullMessage
				if exception != None:
					print traceback.format_exc()
			
			if level <= logLevel and __logDirectory != None and __logFileName != None:
				currentDate = time.strftime("%Y-%m-%d")
				if __logFile == None or currentDate != __logCurrentDate:
					if __logFile != None:
						__logFile.close()
					
					filePath = os.path.join(__logDirectory, __logFileName + '.' + currentDate)
					__logFile = open(filePath, 'a')
					__logCurrentDate = currentDate
				
				__logFile.write("%s\n" % fullMessage)
				if exception != None:
					__logFile.write(traceback.format_exc())
				__logFile.flush()

def fatal(section, message, exception=None):
	report(section, FATAL, message, exception)

def alert(section, message, exception=None):
	report(section, ALERT, message, exception)

def error(section, message, exception=None):
	report(section, ERROR, message, exception)

def warning(section, message, exception=None):
	report(section, WARNING, message, exception)

def info(section, message, exception=None):
	report(section, INFO, message, exception)

def trace(section, message, exception=None):
	report(section, TRACE, message, exception)

def debug(section, message, exception=None):
	report(section, DEBUG, message, exception)
