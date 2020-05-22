import datetime
import time
from wialon import Wialon, WialonError
from flask import Flask
from Exec_report import execute_report


app = Flask(__name__)


@app.route("/<username>", methods=['GET'])
def index(username):

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
    callback_retr = ''

    callback_retr += str(callback[0]['c'][0]) + ';'
    callback_retr += str(callback[0]['c'][1]) + ';'
    callback_retr += str(callback[0]['c'][2]) + ';'
    callback_retr += str(callback[0]['c'][3]) + ';'
    callback_retr += str(callback[0]['c'][4]) + ';'
    callback_retr += str(callback[0]['c'][5]) + ';'

    return callback_retr


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4567, debug=True, threaded=True)

