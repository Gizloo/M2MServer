# -*- coding: utf-8 -*-
import datetime
import time
from wialon import Wialon, WialonError
from flask import Flask
from Exec_report import execute_report
from down_data import api_wialon_dwnData
from handler import handler

app = Flask(__name__)


@app.route("/KrayDEO/<requestbot>", methods=['GET'])
def index(requestbot):
    req_b = str(requestbot)
    print(req_b)
    token, ID, TimeFrom, TimeTo = req_b.split(';')
    y, m, d, h, min, s = TimeFrom.split('-')
    y1, m1, d1, h1, min1, s1 = TimeTo.split('-')
    t1 = datetime.datetime(int(y), int(m), int(d), int(h), int(min), int(s))
    from_time = int(str(time.mktime(t1.timetuple()))[:-2]) - 25200
    t2 = datetime.datetime(int(y1), int(m1), int(d1), int(h1), int(min1), int(s1))
    to_time = int(str(time.mktime(t2.timetuple()))[:-2]) - 25200

    wialon = Wialon()
    login = None
    try:
        login = wialon.token_login(token=str(token))
    except WialonError as e:
        print('Error while login')
    wialon.sid = login['eid']
    res_id = api_wialon_dwnData(wialon)
    #res_id = 21121126
    if res_id:
        calb1, calb2, calb3 = execute_report(res_id, wialon, ID, from_time, to_time)
    else:
        return 'No API resourses'

    milleage = int(str(calb1[1][1])[:calb1[1][1].find("."):])

    callback_retr = ''
    callback_retr += str(calb1[1][1])[:calb1[1][1].find(" "):] + ';'
    callback_retr += str(calb1[2][1]) + ';'
    callback_retr += str(calb1[3][1])[:calb1[3][1].find(" "):] + ';'
    callback_retr += str(calb1[4][1])[:calb1[4][1].find(" "):] + ';'
    callback_retr += str(calb1[5][1])[:calb1[5][1].find(" "):] + ';'
    callback_retr += str(calb1[6][1])[:calb1[6][1].find(" "):] + ';'

    callback = handler(calb2, calb3, milleage)

    callback_retr += str(callback.data_status) + ';' + str(callback.dut_status) + ';' + str(
        callback.track_status) + ';' + str(callback.ign_status) + ';'

    return callback_retr


if __name__ == "__main__":
    app.run(host='10.128.0.2', port=4567, debug=True, threaded=True)
