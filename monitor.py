from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import *
import pytz
from tzlocal import get_localzone
import webbrowser
from scapy.all import *
from time import sleep
from easygui_timerbox import timerbox

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))

print ("Listening ... \n")


def arp_display(pkt):

    if pkt[ARP].op == 1:

        if pkt[ARP].hwsrc == "<mac-address":

            now = datetime.now().isoformat() + 'Z' # 'Z' indicates UTC time
            print('Getting the upcoming 10 events')
            events_result = service.events().list(calendarId='primary', timeMin=now,
                                                  maxResults=10, singleEvents=True,
                                                  orderBy='startTime').execute()
            events = events_result.get('items', [])

            time_now = datetime.now()
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                try:
                    time = datetime.strptime(start[:19], '%Y-%m-%dT%H:%M:%S')
                    time_end = datetime.strptime(end[:19], '%Y-%m-%dT%H:%M:%S')
                    if (abs(time-time_now).total_seconds()<=300) or (time_now > time and time_now< time_end ):
                        link = event['hangoutLink']

                        webbrowser.open(link)
			sleep(200) #To avoid taking multiple input
                    else:
                        timerbox('No meeting now', 'Monitor', time=10)
			sleep(20)
                except BaseException as e:
                    timerbox('Error', 'Monitor', time=10)
		



sniff(prn=arp_display, filter="arp", store=0)
