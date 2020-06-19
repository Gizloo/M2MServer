import datetime
from pprint import pprint

from wialon import Wialon, WialonError, flags

token = 'e5023bcf1b3d6fa822c0f3b8d03759d5C81B9FB7768294A92AD2138C5F516C26FF757672'
wialon = Wialon()
login = None
try:
    login = wialon.token_login(token=str(token))
except WialonError as e:
    print('Error while login')
wialon.sid = login['eid']


def api_wialon_dwnData(wialon):
    spec = {
        'itemsType': 'avl_unit',
        'propName': 'sys_name',
        'propValueMask': '*',
        'sortType': 'sys_name'
    }

    interval = {"from": 0, "to": 0}
    custom_flag = flags.ITEM_DATAFLAG_BASE
    data = wialon.core_search_items(spec=spec, force=1, flags=custom_flag, **interval)
    return data


data = api_wialon_dwnData(wialon)
pprint(data)
timeFrom = 1590944400
timeTo = 1592326740

unit1 = wialon.messages_load_interval({

    "itemId": 21092790,
    "timeFrom": timeFrom,
    "timeTo": timeTo,
    "flags": 0x0000,
    "flagsMask": 0xFF00,
    "loadCount": 0xffffffff})

# pprint(unit1)
mess_block = unit1['messages']
first_mess_coord_x = None
first_mess_coord_y = None

for mess in mess_block:
    if mess['pos']['x']:
        first_mess_coord_x = mess['pos']['x']
        first_mess_coord_y = mess['pos']['y']
        break

prostrel = 0
prostrel_time = []
print(first_mess_coord_x)
print(first_mess_coord_y)

for mess in mess_block:
    if mess['pos']['x']:
        dist = ((((mess['pos']['x']) - first_mess_coord_x)**2+((mess['pos']['y']) - first_mess_coord_y)**2)**0.5)*70000
        if dist > 400:
            prostrel += 1

            time_mess1 = mess['t']
            time_mess = datetime.datetime.utcfromtimestamp(time_mess1+25200).strftime('%Y-%m-%dT%H:%M:%SZ')

            time_mess = time_mess.replace('Z', ' ')
            time_mess = time_mess.replace('T', ' ')

            prostrel_time.append(str(time_mess)[:20:])
            prostrel_time.append(time_mess1)

        first_mess_coord_x = mess['pos']['x']
        first_mess_coord_y = mess['pos']['y']

print(prostrel)
print(prostrel_time)
