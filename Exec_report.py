# -*- coding: utf-8 -*-


def execute_report(res_id, wialon, id, t1, t2):

    units1 = None
    units2 = None
    units3 = None
    units4 = None
    #print(t1)
    #print(t2)

    units = wialon.report_exec_report({
        'reportResourceId': res_id,
        'reportTemplateId': 1,
        'reportObjectId': id,
        'reportObjectSecId': 0,
        'interval': {'from': t1, 'to': t2, 'flags': 0}})
    # pprint(units)
    units = units['reportResult']['stats']
    try:
        units1 = wialon.report_get_result_rows({
             "tableIndex": 0,
             "indexFrom": 0,
             "indexTo": 0
            })
        try:
            units2 = wialon.report_get_result_rows({
                 "tableIndex": 1,
                 "indexFrom": 0,
                 "indexTo": 0
            })

        except:
            pass
    except:
        pass
    return units, units1, units2
