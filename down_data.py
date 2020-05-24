from pprint import pprint

from wialon import flags, Wialon


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
    # pprint(data)
    res_id = None
    for count in data['items']:
        if '_api' in str(count['nm']):
            res_id = count['id']
    return res_id