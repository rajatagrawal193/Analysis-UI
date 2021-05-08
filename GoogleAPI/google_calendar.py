from __future__ import print_function
from datetime import datetime, timedelta, timezone
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


class CalendarService:
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

    def build_service(self):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    '/Users/rajatagrawal/work/analysis/Frontend/GoogleAPI/credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('calendar', 'v3', credentials=creds)
        return service

    def __init__(self):
        self.service = self.build_service()

    def get_events(self, calendar_id, start_date, end_date):
        now = datetime.utcnow()
        one_week_before = now - timedelta(days=30)
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        one_week_before = one_week_before.isoformat() + 'Z'
        # time_min = start_date
        time_min = datetime.fromisoformat(start_date).isoformat() + 'Z'
        time_max = datetime.fromisoformat(end_date).isoformat() + 'Z'
        # 'gc1r2v6buaavim8o14bkd61r7g@group.calendar.google.com'
        print("getting events from calendar")
        events_result = self.service.events().list(calendarId=calendar_id,
                                                   timeMin=time_min,
                                                   timeMax=time_max,
                                                   singleEvents=True,
                                                   orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        result = []
        for event in events:
            temp = {}
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            temp['start'] = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S+05:30')
            temp['end'] = datetime.strptime(end, '%Y-%m-%dT%H:%M:%S+05:30')
            temp['summary'] = event['summary']
            result.append(temp)
        return result


if __name__ == '__main__':
    pass
    calendar = CalendarService()
    result = calendar.get_events("gc1r2v6buaavim8o14bkd61r7g@group.calendar.google.com", '2021-04-01', '2021-05-01')

    print(result)

