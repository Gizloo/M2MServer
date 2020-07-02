# -*- coding: utf-8 -*-

def handler1(calb2, calb3, mill, pr_count, pr_dist):
    class callback:
        def __init__(self):
            self.data_status = 'Data Ok (>90%)'
            self.track_status = 'Track Ok (>90%)'
            self.dut_status = 'DUT no Error'
            self.ign_status = 'IGN no Error'

    callback = callback()

    if calb2:
        if calb2[0]['c'][0] == 'ДУТ не работает':
            h, m, s = calb2[0]['c'][4].split(':')
            if int(calb2[0]['c'][3]) > 10 and int(h) > 1:
                callback.dut_status = 'Lost DUT data (>10%)'
        else:
            h, m, s = str(calb2[0]['c'][2]).split(':')
            if int(h) > 1:
                callback.data_status = 'Lost data ( >10% )'

    if calb3:
        if calb3[0]['c'][0] == 'ДУТ не работает':
            h, m, s = calb3[0]['c'][4].split(':')
            if int(calb3[0]['c'][3]) > 10 and int(h) > 1:
                callback.dut_status = 'DUT Error ( >10% )'

    if pr_count > 1 and pr_dist > int(mill)/100*85:
        callback.track_status = 'Track NotOk (<90%)'

    return callback


def handler2(volume_tank, consum_f, fuel_up_f, fuel_down, fuel_up_n, consum_n, start_fuel_p, start_fuel_f):

    class callback2:
        def __init__(self):
            self.fuel_start = False
            self.fuel_down = False
            self.fuel_up = False
            self.short = False
            self.perejog = False
            self.economy = False
            self.nedoliv = False

    callback2 = callback2()
    if int(fuel_down) > 0:
        callback2.fuel_down = True
    diff_f = fuel_up_f - fuel_up_n
    pr_diff_f = int(diff_f / volume_tank * 100)
    if pr_diff_f > 2:
        callback2.fuel_up = True
    if pr_diff_f < -2:
        callback2.nedoliv = True
    diff_fuel_start = int(start_fuel_f - start_fuel_p)
    if diff_fuel_start > 5 or diff_fuel_start < -5:
        callback2.fuel_start = True

    if consum_n / volume_tank * 100 < 5:
        callback2.short = True
    else:
        diff_consum = consum_f - consum_n
        pr_diff_consum = int(diff_consum / volume_tank * 100)
        if pr_diff_consum > 1:
            callback2.perejog = True
        if pr_diff_consum < -1:
            callback2.economy = True

    return callback2


