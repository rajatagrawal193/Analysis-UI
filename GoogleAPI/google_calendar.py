from __future__ import print_function
from datetime import datetime, timedelta, timezone
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from models.calendar_event import CalendarEvent

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

    def set_to_calendar_event(self, event):
        start_dt = event['start'].get('dateTime', event['start'].get('date'))
        end_dt = event['end'].get('dateTime', event['end'].get('date'))
        start = datetime.strptime(start_dt, '%Y-%m-%dT%H:%M:%S+05:30')
        end = datetime.strptime(end_dt, '%Y-%m-%dT%H:%M:%S+05:30')
        summary = event['summary']
        description = event['description'] if 'description' in event else ""
        return CalendarEvent(start, end, summary, description, event)

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
        # result = [Event(event) for event in events]
        result = [self.set_to_calendar_event(event) for event in events]
        # for event in events:
        #     temp = {}
        #     start_dt = event['start'].get('dateTime', event['start'].get('date'))
        #     end_dt = event['end'].get('dateTime', event['end'].get('date'))
        #     start = datetime.strptime(start_dt, '%Y-%m-%dT%H:%M:%S+05:30')
        #     end = datetime.strptime(end_dt, '%Y-%m-%dT%H:%M:%S+05:30')
        #     summary = event['summary']
        #     description = event['description'] if 'description' in event else ""
        #     calendar_event = CalendarEvent(start, end, summary, description, event)
        return result

    def list_calendars(self):
        page_token = None
        while True:
            calendar_list = self.service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                print(calendar_list_entry['summary'],"\n",calendar_list_entry['id'])
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break


if __name__ == '__main__':
    pass
    calendar = CalendarService()
    WORKOUT_CALENDAR_ID = "kfb7kr4iegnkieils995vrbeck@group.calendar.google.com"
    SLEEP_CALENDAR_ID = "gc1r2v6buaavim8o14bkd61r7g@group.calendar.google.com"
    result = calendar.get_events(WORKOUT_CALENDAR_ID, '2021-05-03', '2021-05-09')
    print(result)
    for item in result:
        print(item.start)
    # calendar.list_calendars()


