# local imports
from lib.funcs import *
from lib.config import config
# google imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError
# other imports
import os.path, base64, time
from httplib2.error import ServerNotFoundError
from email.mime.text import MIMEText


# if modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']
CREDS_PATH = convert_path_os('data/config/client_secret.apps.googleusercontent.com.json')


class GmailManager():
	"""
    Purpose - Manage Gmail interactions
    """
	def __init__(self, bot:object) -> None:
		# bot object
		self.bot = bot
		# init auth
		self.auth()
		# default from email
		self.my_email = config['gmail']['gmail_address']


	def auth(self) -> None:
		"""
        Purpose - Gets service options for Google Gmail API
        """
		creds = None
		# The file token.json stores the user's access and refresh tokens, and is
		# created automatically when the authorization flow completes for the first time.
		if os.path.exists('token.json'):
			creds = Credentials.from_authorized_user_file('token.json', SCOPES)
		# If there are no (valid) credentials available, let the user log in.
		if not creds or not creds.valid:
			if creds and creds.expired and creds.refresh_token:
				try:
					creds.refresh(Request())
				except RefreshError as e:
					print(e)
					flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
					creds = flow.run_local_server(port=0)
			else:
				flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
				creds = flow.run_local_server(port=0)
			# Save the credentials for the next run
			with open('token.json', 'w') as token:
				token.write(creds.to_json())
		try:
			# Call the Gmail API
			self.service = build('gmail', 'v1', credentials=creds)

		except HttpError as error:
			# TODO(developer) - Handle errors from gmail API.
			print(f'An error occurred: {error}')


	def send_message(self, msg: str) -> None:
		"""
        Purpose - Sends email using google gmail api

        Param - msg: The message to be sent
        """
		# Create a message
		temp_message = MIMEText(msg)
		temp_message['To'] = self.my_email
		temp_message['From'] = self.my_email
		temp_message['Subject'] = f'Automated From {self.bot.name}'
		# encoded message
		# Send the email
		message = {'raw': base64.urlsafe_b64encode(temp_message.as_bytes()).decode()}
		# Send the email
		try:
		    message = (self.service.users().messages().send(userId="me", body=message).execute())
		except HttpError as error:
		    print(f'An error occurred: {error}')
		except ServerNotFoundError as error:
			print(123)
			print(f'An error occurred: {error}')





