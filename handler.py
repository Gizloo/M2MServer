from pprint import pprint


def handler(calb2, calb3, mill):
    class callback:
        def __init__(self):
            self.data_status = 'Данные есть (90%)'
            self.track_status = 'Трек корректен (90%)'
            self.dut_status = 'Ошибок по ДУТ нет'
            self.ign_status = 'Ошибок по зажиганию нет'
    callback = callback()

    if calb2 is not None:
        if calb2[0]['c'][0] == 'ДУТ не работает':
            h, m, s = calb2[0]['c'][4].split(':')
            if int(calb2[0]['c'][3]) > 10 and int(h) > 0:
                callback.dut_status = 'Потеря данных с ДУТ больше 90%'
        elif calb2[0]['c'][0] == "Превышение расстояния между сообщениями":
            if (int(calb2[0]['c'][3]) * 500 / mill * 1000) * 100 > 10:
                callback.track_status = 'Прострелов (больше 90%)'
        else:
            h, m, s = str(calb2[0]['c'][2]).split(':')
            if int(h) > 0 or int(m) > 58:
                callback.data_status = 'Потеря данных больше 90%'

    if calb3:
        if calb3[0]['c'][0] == 'ДУТ не работает':
            h, m, s = calb3[0]['c'][4].split(':')
            if int(calb3[0]['c'][3]) > 10 and int(h) > 0:
                callback.dut_status = 'Потеря данных с ДУТ больше 90%'
        elif calb2[0]['c'][0] == "Превышение расстояния между сообщениями":
            if (int(calb3[0]['c'][3]) * 500 / mill * 1000) * 100 > 10:
                callback.track_status = 'Прострелов (больше 90%)'

    return callback



