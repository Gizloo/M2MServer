# coding: utf8

from wialon import flags, Wialon


def api_wialon_dwnData(wialon):
    res_id = None
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
