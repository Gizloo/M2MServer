# -*- coding: utf-8 -*-

import datetime
import time
from wialon import Wialon, WialonError
from flask import Flask, render_template
from Exec_report import execute_report, execute_report2
from down_data import api_wialon_dwnData
from handler import handler1, handler2

app = Flask(__name__)


@app.route("/KrayDEO/<requestbot>", methods=['GET'])
def index(requestbot):
    req_b = str(requestbot)
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
    callback_retr += str(calb1[4][1])[:calb1[3][1].find(" "):] + ';'
    callback_retr += str(calb1[3][1])[:calb1[4][1].find(" "):] + ';'
    callback_retr += str(calb1[5][1])[:calb1[5][1].find(" "):] + ';'
    callback_retr += str(calb1[6][1])[:calb1[6][1].find(" "):] + ';'
    callback = handler1(calb2, calb3, milleage, pr_count, pr_dist)

    callback_retr += str(callback.data_status) + ';' + str(callback.track_status) \
                     + ';' + str(callback.dut_status) + ';' + str(callback.ign_status) + ';'

    return callback_retr


@app.route("/KrayDEO/norm/<requesthandler>", methods=['GET'])
def norm(requesthandler):
    req_b = str(requesthandler)

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
        callback_retr += "Заправка не сходится:" + str(round(fuel_up_f - fuel_up, 2)) + ";"
    elif callback.nedoliv:
        callback_retr += "Недолив:" + str(round((fuel_up - fuel_up_f), 2)) + ";"
    else:
        callback_retr += "Ok;"  # Заправка ОК

    if callback.fuel_down:
        callback_retr += str(round(fuel_down, 2)) + ";"
    else:
        callback_retr += "0;"  # Слив ОК

    if callback.fuel_start:
        callback_retr += "Нач ур. не сходится!;"
    else:
        callback_retr += "Ok;"  # Нач ур. ОК

    """Дальше один из 4 вариантов"""
    if callback.short:
        callback_retr += "Короткая поездка, списание по норме;"

    elif callback.perejog:
        callback_retr += "Пережог топлива:" + str(round(consum_f - consumption_n, 2)) + ", списание по факту;"

    elif callback.economy and not callback.nedoliv and not callback.fuel_down:
        callback_retr += "Экономия топлива:" + str(round(consumption_n - consum_f, 2)) + ", списание по факту;"

    else:
        callback_retr += "Расход сходится"

    return callback_retr


@app.route("/KrayDEO/test/<requestbot>", methods=['GET'])
def test(requestbot):
    req_b = str(requestbot)
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
    probeg = calb1[1][1].replace("km", 'км.')
    callback_retr += str(calb1[2][1]) + ';'
    motoh = calb1[2][1]
    callback_retr += str(calb1[4][1])[:calb1[4][1].find(" "):] + ';'
    start_fuel = calb1[4][1].replace("l", 'л.')

    callback_retr += str(calb1[3][1])[:calb1[3][1].find(" "):] + ';'
    end_fuel = calb1[3][1].replace("l", 'л.')

    callback_retr += str(calb1[5][1])[:calb1[5][1].find(" "):] + ';'
    fuel_up = calb1[5][1].replace("l", 'л.')
    callback_retr += str(calb1[6][1])[:calb1[6][1].find(" "):] + ';'
    fuel_down = calb1[6][1].replace("l", 'л.')
    callback = handler1(calb2, calb3, milleage, pr_count, pr_dist)

    callback_retr += str(callback.data_status) + ';' + str(callback.track_status) \
                     + ';' + str(callback.dut_status) + ';' + str(callback.ign_status) + ';'

    data_obj = wialon.core_search_item({"id": ID, "flags": 0x00000001})
    name_obj = data_obj['item']['nm']
    start_period = f'{d}.{m}.{y}. {h}:{min}:{s}'
    end_period = f'{d1}.{m1}.{y1}. {h1}:{min1}:{s1}'
    return render_template('test_first.html', name=name_obj, probeg=probeg, motoh=motoh, start_fuel=start_fuel,
                           end_fuel=end_fuel, fuel_up=fuel_up, fuel_down=fuel_down, start_period=start_period,
                           end_period=end_period, data_status=callback.data_status, track_status=callback.track_status,
                           dut_status=callback.dut_status, ign_status=callback.ign_status, callback_full=callback_retr)



@app.route("/KrayDEO/test_norm/<requesthandler>", methods=['GET'])
def test_norm(requesthandler):

    req_b = str(requesthandler)
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
        callback_retr += "Заправка не сходится:" + str(round(fuel_up_f - fuel_up, 2)) + ";"
    elif callback.nedoliv:
        callback_retr += "Недолив:" + str(round((fuel_up - fuel_up_f), 2)) + ";"
    else:
        callback_retr += "Ok;"  # Заправка ОК

    if callback.fuel_down:
        callback_retr += str(round(fuel_down, 2)) + ";"
    else:
        callback_retr += "0;"  # Слив ОК

    if callback.fuel_start:
        callback_retr += "Нач ур. не сходится!;"
    else:
        callback_retr += "Ok;"  # Нач ур. ОК

    """Дальше один из 4 вариантов"""
    if callback.short:
        callback_retr += "Короткая поездка, списание по норме;"

    elif callback.perejog:
        callback_retr += "Пережог топлива:" + str(round(consum_f - consumption_n, 2)) + ", списание по факту;"

    elif callback.economy and not callback.nedoliv and not callback.fuel_down:
        callback_retr += "Экономия топлива:" + str(round(consumption_n - consum_f, 2)) + ", списание по факту;"

    else:
        callback_retr += "Расход сходится"

    return callback_retr


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4567, debug=True, threaded=True)
