from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# OAuth-Scope
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=8081, open_browser=False)
    return creds

def create_event(creds, event):
    service = build('calendar', 'v3', credentials=creds)
    event_result = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Event created: {event_result.get('htmlLink')}")

if __name__ == '__main__':
    creds = authenticate_google()
    example_event = {
        'summary': 'Meeting with Team',
        'description': 'Discuss project status',
        'start': {'dateTime': '2025-05-10T10:00:00', 'timeZone': 'Europe/Zurich'},
        'end': {'dateTime': '2025-05-10T12:00:00', 'timeZone': 'Europe/Zurich'},
    }
    create_event(creds, example_event)
