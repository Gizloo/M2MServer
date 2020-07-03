from wialon import flags, Wialon, WialonError


token = 'db1cee3b1f964df20f8d163a1423b6c6286A919144720D152383E5DD77C6113AD31CDC9A'
wialon = Wialon()
login = None
try:
    login = wialon.token_login(token=str(token))
except WialonError as e:
    print('Error while login')
wialon.sid = login['eid']
res_id = wialon.core_search_item({"id": 21154797, "flags": 0x00000001})
print(res_id)
