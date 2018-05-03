# Imports
# # Python compatibility
from __future__ import print_function
# # Built-in
import os
import json
import logging
# # External
# # # Signature template rendering
from jinja2 import Environment, FileSystemLoader, select_autoescape
# # # Google APIs
from apiclient.discovery import build
from google.oauth2 import service_account

# Constants
USERS_FILE = "users.json"
"""
    str: path to the users' information file
"""
SIGNATURE_FOLDER = "_includes"
"""
    str: path to the folder where the signature is located
"""
SIGNATURE_FILE = "signature.html"
"""
    str: name of the signature template in HTML
"""
SCOPES = ['https://www.googleapis.com/auth/gmail.settings.basic',
          'https://www.googleapis.com/auth/gmail.settings.sharing']
"""
    list: list of strings that limit the scope of the Google API queries
"""
SERVICE_ACCOUNT_FILE = "service_account.json"
"""
    str: path to the service account file with credentials to query the
         Google API. This credentials must be domain-wide to impersonate and
         change other users' signatures
"""

# 0. Pre-execution
logging.basicConfig(format="%(asctime)s %(levelname)8s %(message)s",
                    level=logging.INFO)
logging.info("Google Suite - Email signature changer")

# 1. Load users information
logging.info("Loading users information from \"%s\"" % USERS_FILE)
users = json.load(open(USERS_FILE))

# 2. Load signature HTML template
# # Load environment
env = Environment(
    loader=FileSystemLoader(os.path.join(
        os.path.dirname(__file__), SIGNATURE_FOLDER)),
    autoescape=select_autoescape(['html'])
)

# # Load template
logging.info("Loading signature template from \"%s\"" % SIGNATURE_FILE)
template = env.get_template(SIGNATURE_FILE)

# 3. Prepare Google APIs
logging.info("Creating Google credentials object from file \"%s\"" %
             SERVICE_ACCOUNT_FILE)
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# 4. Loop each user
logging.info("All ready, will start applying signatures")
for user, user_info in users.iteritems():
    logging.info("--- %s ---" % user)

    # Create delegated credentials
    delegated_credentials = credentials.with_subject(user)

    # Create service
    service = build('gmail', 'v1', credentials=delegated_credentials)

    # Render signature based on template
    signature = template.render(user_info)

    # Update signature
    results = service.users().settings().sendAs().update(
        sendAsEmail=user,
        userId="me",
        body={"signature": signature}).execute()
