import datetime
import time
from pprint import pprint

from wialon import Wialon, WialonError
from flask import Flask
from Exec_report import execute_report

username = "20914243;2020-05-21-0-0-0;2020-05-21-16-40-0"

ID, TimeFrom, TimeTo  = username.split(';')

y, m, d, h, min, s = TimeFrom.split('-')
y1, m1, d1, h1, min1, s1 = TimeTo.split('-')
t1 = datetime.datetime(int(y), int(m), int(d), int(h), int(min), int(s))
from_time = int(str(time.mktime(t1.timetuple()))[:-2])
t2 = datetime.datetime(int(y1), int(m1), int(d1), int(h1), int(min1), int(s1))
to_time = int(str(time.mktime(t2.timetuple()))[:-2])
wialon = Wialon()
login = None

try:
    login = wialon.token_login(token='db1cee3b1f964df20f8d163a1423b6c64C075B1F934CEB40832DB0C714AA88C6F621F8D5')
except WialonError as e:
    print('Error while login')

wialon.sid = login['eid']
callback = execute_report(wialon, ID, from_time, to_time)
pprint(callback)
print(callback[0]['c'][0])