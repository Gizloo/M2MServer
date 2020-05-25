# -*- coding: utf-8 -*-

from pprint import pprint


def handler(calb2, calb3, mill):
    class callback:
        def __init__(self):
            self.data_status = 'Data is correct (90%)'
            self.track_status = 'Track is correct (90%)'
            self.dut_status = 'No DUT error'
            self.ign_status = 'No IGN error'

    callback = callback()

    if calb2:
        if calb2[0]['c'][0] == 'ДУТ не работает':
            h, m, s = calb2[0]['c'][4].split(':')
            if int(calb2[0]['c'][3]) > 10 and int(h) > 0:
                callback.dut_status = 'Lost DUT data (>10%)'

        elif calb2[0]['c'][0] == "Превышение расстояния между сообщениями":

            if (int(calb2[0]['c'][3]) * 500 / mill * 1000) * 100 > 10:
                callback.track_status = 'Track isnt correct ( >10% )'
        else:
            h, m, s = str(calb2[0]['c'][2]).split(':')
            if int(h) > 0 or int(m) > 58:
                callback.data_status = 'Lost data ( >10% )'

    if calb3:
        if calb3[0]['c'][0] == 'ДУТ не работает':
            h, m, s = calb3[0]['c'][4].split(':')
            if int(calb3[0]['c'][3]) > 10 and int(h) > 0:
                callback.dut_status = 'Lost DUT data ( >10% )'
        elif calb2[0]['c'][0] == "Превышение расстояния между сообщениями":
            if (int(calb3[0]['c'][3]) * 500 / mill * 1000) * 100 > 10:
                callback.track_status = 'Lost data ( >10% )'

    return callback



