# local packages
from lib.funcs import *
from lib.web_funcs.ada_fruit_manager import AdaFruitManager
from lib.web_funcs.gmail_manager import GmailManager
# other imports
import datetime, time, logging, traceback, platform
from typing import Optional


# Get the operating system name
OS_TYPE = platform.system().lower()

# logging.basicConfig(level=logging.DEBUG)
# LOGGER = logging.getLogger(__name__)


""" ------------------------------------------ Bot Instance ------------------------------------------------ """
class Bot():
	"""
	Purpose - Webscappering bot object that parsers for ada fruit stock
	"""
	def __init__(self) -> None:
		# name of bot
		self.name = 'Ada Fruit Bot'
		# testing state
		self.testing_state = False
		# alerts
		self.alerts = False if self.testing_state else True
		# html finder 
		self.ada_fruit_manager = AdaFruitManager(OS_TYPE, self.testing_state)
		# gmail manager
		self.email_manager = GmailManager(self)
		
		

	""" ------------------------------------------ Error Handle Methods ------------------------------------------------ """
	def send_embed_error(self, message:str) -> None:
		"""
		Purpose - Get and send script info to default url

		Param - message: String to send
		"""
		self.email_manager.send_message(f'Ada Fruit Bot went offline due to the following error:\n{message}')


	""" ------------------------------------------ Update Methods ------------------------------------------------ """
	def run(self, version:str, product:str) -> None:
		"""
		Purpose - Ada fruit used to purchase raspi

		Param - version: Verison of Bot

		Param - product: Product name
		"""
		# version prompt 
		print(f"Version: {version}")
		# program loop
		while True:
			# attempt to scrape ada fruit
			try:
				# attempt to purchase product
				if self.ada_fruit_manager.ada_fruit_purchase():
					# if alerts
					if self.alerts:
						# send email about purchase
						self.email_manager.send_message(f'Ada Fruit Bot Purchased a {product}')
			# except errors and print
			except Exception as e:
				# if alerts
				if self.alerts:
					# send stopped prompt
					self.send_embed_error(f'{str(type(e))}\n{e}')
				# raise error
				raise(e)

# bot
bot = Bot()
