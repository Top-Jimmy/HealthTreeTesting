
class Error(Exception):
	'''Base class for custom exceptions'''
	pass

class MsgError(Error):
	'''Raised when error msg is found after form submission'''
	pass

class WarningError(Error):
	'''Raised when input has warning after form submission'''

