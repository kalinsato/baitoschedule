from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def readschedule():
    f = open('schedule.txt', encoding='utf-8', mode="r")
    data1 = f.read()
    lines1 = data1.split('\n') 
    f.close()
    return lines1

def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    readschedule()
    print(readschedule())

    yearmon = readschedule()[-1]
    a = yearmon.split(".")
    year = int(a[0])
    mon = int(a[1])

    if mon == 1 or mon == 3 or mon == 5 or mon == 7 or mon == 8 or mon == 10 or mon == 12:
        num_days = 31
    elif mon == 2:
        num_days = 28
    else :
        num_days = 30

    for i in readschedule():
        s = i.split(' ')
        if(len(s) == 1): continue

        d_s = int(s[0])
        d_e = int(s[0])
        t1_s = int(s[1])
        t2_s = int(s[2])
        t1_e = int(s[3])
        t2_e = int(s[4])
        m_s = mon
        m_e = mon
        y_s = year
        y_e = year

        if(mon == 12 and d_e == 31): 
            y_e = year + 1

        if(num_days == d_e):
            d_e = 1
            if mon == 12: m_e = 1
            else: m_e = m_e + 1 



        event = {
        'summary': 'バイト',
        'location': 'baito',
        'description': '{}'.format(s[1]),
        'start': {
            'dateTime': datetime.datetime(y_s,m_s,d_s,t1_s, t2_s).isoformat(),
            'timeZone': 'Japan'
        },
        'end': {
            'dateTime': datetime.datetime(y_e,m_e,d_e,t1_e,t2_e).isoformat(),
            'timeZone': 'Japan'
        },
        }
        event = service.events().insert(calendarId='<id>',body=event).execute()
        print (event['id'])

if __name__ == '__main__':
    main()