import os, datetime, platform

# Get the operating system name
OS_TYPE = platform.system().lower()
SCRIPT_START = datetime.datetime.now()

""" ------------------------------------------ File System Funcs ------------------------------------------------ """
def get_file_names(path: str) -> list:
	"""
	Purpose - Get a list of subdircetory names in a given path

	Param - path: Path to extract subdirectory names
	"""
	return os.listdir(path)
	
def convert_path_os(path: str) -> str:
	"""
	Purpose - Converts path to standard format based on os type

	Param - path: Path to change to the proper format based on platform
	"""
	return path.replace('\\','/') if OS_TYPE == 'linux' or OS_TYPE == 'darwin' else path.replace('/','\\')



