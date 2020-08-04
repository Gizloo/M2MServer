# -*- coding: utf-8 -*-

from pprint import pprint

from wialon import flags, Wialon, WialonError


def api_wialon_dwnData(wialon):
    spec = {
        'itemsType': 'avl_resource',
        'propName': 'sys_name',
        'propValueMask': '*',
        'sortType': 'sys_name'
    }
    interval = {"from": 0, "to": 0}
    custom_flag = flags.ITEM_DATAFLAG_BASE
    data = wialon.core_search_items(spec=spec, force=1, flags=custom_flag, **interval)
    res_id = None
    for count in data['items']:
        if 'api' in str(count['nm']):
        	res_id = count['id']
   
    return res_id


def api_wialon_dwnObj(wialon):
    spec = {
        'itemsType': 'avl_unit',
        'propName': 'sys_name',
        'propValueMask': '*',
        'sortType': 'sys_name'
    }
    interval = {"from": 0, "to": 0}
    custom_flag = flags.ITEM_DATAFLAG_BASE + 0x00000100
    data = wialon.core_search_items(spec=spec, force=1, flags=custom_flag, **interval)
    pprint(data)
    for key in data['items']:
        # print(f'{key["nm"]} : {key["id"]}')
        print(key)


token = 'd3ff2792689e2584f97d38ca51893d6f43598232EC622405C8D74152117122D4A40A7CF7'
wialon = Wialon()
login = None
try:
    login = wialon.token_login(token=str(token))
except WialonError as e:
    print('Error while login')
wialon.sid = login['eid']
api_wialon_dwnObj(wialon)
