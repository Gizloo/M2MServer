import datetime
import time
from pprint import pprint
from  down_data import api_wialon_dwnData
from wialon import Wialon, WialonError
from flask import Flask
from Exec_report import execute_report
from handler import handler

username = "20914243;2020-05-21-08-00-00;2020-05-21-20-00-00"

token = 'db1cee3b1f964df20f8d163a1423b6c60314BB8E0E3A5135B336096AAEF0C4346AAF14A0'
ID, TimeFrom, TimeTo = username.split(';')
y, m, d, h, min, s = TimeFrom.split('-')
y1, m1, d1, h1, min1, s1 = TimeTo.split('-')
t1 = datetime.datetime(int(y), int(m), int(d), int(h), int(min), int(s))
from_time = int(str(time.mktime(t1.timetuple()))[:-2])
t2 = datetime.datetime(int(y1), int(m1), int(d1), int(h1), int(min1), int(s1))
to_time = int(str(time.mktime(t2.timetuple()))[:-2])

wialon = Wialon()
login = None

try:
    login = wialon.token_login(token=token)
except WialonError as e:
    print('Error while login')

wialon.sid = login['eid']
res_id = api_wialon_dwnData(wialon)
calb1, calb2, calb3 = execute_report(res_id, wialon, ID, from_time, to_time)
# pprint(calb2)
# print(calb2[0]['c'][2])

milleage = int(str(calb1[1][1])[:calb1[1][1].find("."):])
pprint(calb1)

callback_retr = ''
callback_retr += str(calb1[1][1])[:calb1[1][1].find(" "):] + ';'
callback_retr += str(calb1[2][1]) + ';'
callback_retr += str(calb1[3][1])[:calb1[3][1].find(" "):] + ';'
callback_retr += str(calb1[4][1])[:calb1[4][1].find(" "):] + ';'
callback_retr += str(calb1[5][1])[:calb1[5][1].find(" "):] + ';'
callback_retr += str(calb1[6][1])[:calb1[6][1].find(" "):] + ';'

callback = handler(calb2, calb3, milleage)
callback_retr += str(callback.data_status) + ';' + str(callback.dut_status) + ';' + str(callback.track_status) + ';' + str(callback.ign_status) + ';'
# print(obj_callback)
print(callback_retr)
# print(callback[0]['c'][0])

