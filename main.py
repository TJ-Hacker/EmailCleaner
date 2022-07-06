from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

collegeKeywords = ["admissions", "college", "university"]

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    app(creds)


def app(_creds):
    creds = _creds
    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me').execute()

        messages = results.get('messages', [])

        if not messages:
            print('No mail found.')
            return
        print('Mail:')
        for message in messages:
            if checkMailSnippet(service, message['id']):
                addLabel(service, message['id'])

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')

def checkMailSnippet(serv, _id):
    service = serv
    mess = service.users().messages().get(userId='me', id=_id).execute()
    snippet = mess["snippet"].lower()
    subject = ""

    headers = mess["payload"]["headers"]

    for header in headers:
        if header["name"] == "Subject":
            subject = header["value"].lower()


    for keyword in collegeKeywords:
        if keyword in snippet:
            return True

    for keyword in collegeKeywords:
        if keyword in subject:
            return True

    return False

def labelInit(serv):
    sevice = serv
    labels = service.users.labels.list(userId='me').execute()["labels"]
    labelExists = False
    for label in labels:
        if label == "College":
            labelExists = True

    # Finish later

# Add College Label to email
def addLabel(serv, _id):
    service = serv
    request = {"addLabelIds": ["College"]}
    service.users().messages().modify(userId='me', id=_id, body=request).execute()

if __name__ == '__main__':
    main()
