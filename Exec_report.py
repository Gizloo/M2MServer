
def execute_report(wialon, id, t1, t2):
    print(t1)
    print(t2)

    units = wialon.report_exec_report({
        'reportResourceId': 12824465,
        'reportTemplateId': 5,
        'reportObjectId': id,
        'reportObjectSecId': 0,
        'interval': {'from': t1, 'to': t2, 'flags': 0}})

    try:
         units1 = wialon.report_get_result_rows({
             "tableIndex": 0,
             "indexFrom": 0,
             "indexTo": 0
         })
         return units1
    except Exception as exc:
         return 'Невозможно загрузить отчет'