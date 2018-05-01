# Imports
from __future__ import print_function
import os
import json
from jinja2 import Environment, FileSystemLoader, select_autoescape, Template
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


# Load environment
env = Environment(
	loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'signatures')),
	autoescape=select_autoescape(['html'])
)

# Load template
template = env.get_template('generic@btcassessors.com.html')

# Load data
data = json.load(open('data.json'))

# Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.settings.basic','https://www.googleapis.com/auth/gmail.settings.sharing',
	 'https://mail.google.com/', 'https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/gmail.compose',
	 'https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.metadata']
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('gmail', 'v1', http=creds.authorize(Http()))

# Get user profile
user_profile = service.users().getProfile(userId="me").execute()

# Get signature rendered
signature = template.render(data[user_profile["emailAddress"]])

# actualitzar signatura
results = service.users().settings().sendAs().update(sendAsEmail=user_profile["emailAddress"], userId="me", body={"signature":signature}).execute()
