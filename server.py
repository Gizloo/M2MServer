# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

import datetime
import time
from wialon import Wialon, WialonError
from flask import Flask
from Exec_report import execute_report, execute_report2
from down_data import api_wialon_dwnData
from handler import handler1, handler2

app = Flask(__name__)


@app.route("/KrayDEO/<requestbot>", methods=['GET'])
def index(requestbot):
    req_b = str(requestbot)
    # print(req_b)
    token, ID, TimeFrom, TimeTo = req_b.split(';')
    y, m, d, h, min, s = TimeFrom.split('-')
    y1, m1, d1, h1, min1, s1 = TimeTo.split('-')
    t1 = datetime.datetime(int(y), int(m), int(d), int(h), int(min), int(s))
    from_time = int(str(time.mktime(t1.timetuple()))[:-2])
    t2 = datetime.datetime(int(y1), int(m1), int(d1), int(h1), int(min1), int(s1))
    to_time = int(str(time.mktime(t2.timetuple()))[:-2])

    wialon = Wialon()
    login = None
    try:
        login = wialon.token_login(token=str(token))
    except WialonError as e:
        print('Error while login')
    wialon.sid = login['eid']
    res_id = api_wialon_dwnData(wialon)

    if res_id:
        calb1, calb2, calb3, pr_count, pr_dist = execute_report(res_id, wialon, ID, from_time, to_time)
    else:
        return 'No API resourses'

    milleage = int(str(calb1[1][1])[:calb1[1][1].find("."):])

    callback_retr = ''
    callback_retr += str(calb1[1][1])[:calb1[1][1].find(" "):] + ';'
    callback_retr += str(calb1[2][1]) + ';'
    callback_retr += str(calb1[3][1])[:calb1[3][1].find(" "):] + ';'

    callback = handler1(calb2, calb3, milleage, pr_count, pr_dist)

    callback_retr += str(callback.data_status) + ';' + str(callback.track_status) \
                     + ';' + str(callback.dut_status) + ';' + str(callback.ign_status) + ';'

    return callback_retr


@app.route("/KrayDEO/norm/<requesthandler>", methods=['GET'])
def norm(requesthandler):
    req_b = str(requesthandler)
    print(req_b)

    token, ID, TimeFrom, TimeTo, start_fuel_n, consumption_n, fuel_up = req_b.split(';')

    start_fuel_n.replace(',', '.')
    consumption_n.replace(',', '.')
    fuel_up.replace(',', '.')

    start_fuel_n, consumption_n, fuel_up = float(start_fuel_n), float(consumption_n), float(fuel_up)

    y, m, d, h, min, s = TimeFrom.split('-')
    y1, m1, d1, h1, min1, s1 = TimeTo.split('-')
    t1 = datetime.datetime(int(y), int(m), int(d), int(h), int(min), int(s))
    from_time = int(str(time.mktime(t1.timetuple()))[:-2])
    t2 = datetime.datetime(int(y1), int(m1), int(d1), int(h1), int(min1), int(s1))
    to_time = int(str(time.mktime(t2.timetuple()))[:-2])

    print(from_time)
    print(to_time)

    wialon = Wialon()
    login = None
    try:
        login = wialon.token_login(token=str(token))
    except WialonError as e:
        print('Error while login')
    wialon.sid = login['eid']
    res_id = api_wialon_dwnData(wialon)

    if res_id:
        volume_tank, end_fuel_f, fuel_up_f, fuel_down, start_fuel_f = execute_report2(res_id, wialon, ID, from_time, to_time)
    else:
        return 'No API resourses'

    consum_f = round(start_fuel_n + fuel_up - end_fuel_f, 2)

    callback = handler2(volume_tank, consum_f, fuel_up_f, fuel_down, fuel_up, consumption_n, start_fuel_n, start_fuel_f)
    callback_retr = ''

    if callback.fuel_up:
        callback_retr += f"Заправка не сходится:{round(fuel_up_f - fuel_up, 2)});"
    elif callback.nedoliv:
        callback_retr += f"Недолив:{round((fuel_up - fuel_up_f), 2)};"
    else:
        callback_retr += "Ok;"  # Заправка ОК

    if callback.fuel_down:
        callback_retr += f"{round(fuel_down, 2)};"
    else:
        callback_retr += "0;"  # Слив ОК

    if callback.fuel_start:
        callback_retr += "Нач ур. не сходится!;"
    else:
        callback_retr += "Ok;"  # Нач ур. ОК

    """Дальше один из 4 вариантов"""
    if callback.short:
        callback_retr += f"Короткая поездка, списание по норме;"

    elif callback.perejog:
        callback_retr += f"Пережог топлива:{round(consum_f - consumption_n, 2)}, списание по факту;"

    elif callback.economy and not callback.nedoliv and not callback.fuel_down:
        callback_retr += f"Экономия топлива:({round(consumption_n - consum_f, 2)}), списание по факту;"

    else:
        callback_retr += f"Расход сходится"

    return callback_retr


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4567, debug=True, threaded=True)
