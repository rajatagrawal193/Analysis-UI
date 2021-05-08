from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
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

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow()
    one_week_before = now - datetime.timedelta(days=2)
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    one_week_before = one_week_before.isoformat() + 'Z'

    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='gc1r2v6buaavim8o14bkd61r7g@group.calendar.google.com', timeMin=one_week_before,
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        # print(event)
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        start = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S+05:30')
        end = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M:%S+05:30')
        print(start, end, event['summary'])
        print("")

    # List all the calendars
    # page_token = None
    # while True:
    #     calendar_list = service.calendarList().list(pageToken=page_token).execute()
    #     for item in calendar_list['items']:
    #         print(item)
    #         print("")
    #     # for calendar_list_entry in calendar_list['items']:
    #     #     print (calendar_list_entry['summary'])
    #     page_token = calendar_list.get('nextPageToken')
    #     if not page_token:
    #         break

if __name__ == '__main__':
    main()
