from pprint import pprint

import requests

from data import json_vtb, res_fssp_vtb
from main import data_requisites
from passwords import token_ofdata

a = data_requisites(json_vtb)


# ogrn = (a['ogrn'])
# ogrn = '1157232015830'
def zapros():
    url = f'https://api.ofdata.ru/v2/enforcements?key={token_ofdata}&ogrn={ogrn}&sort=-date'
    response = requests.get(url).json()
    print(response['meta'])
    return response


def fssp(my_dict):
    if len(my_dict['data']['Записи']) == 0:
        print('Исполнительные производства не ведутся')
    else:
        a = my_dict['data']['ОбщКолич']
        b = my_dict['data']['ОбщСум']
        print(
            f'В отношении компании ведется {a} исполнительных производств на общую сумму {b} рублей')
        print(my_dict['meta'])


# fssp(res_fssp_vtb)

# zapros()

# fssp(zapros())

pprint(res_fssp_vtb)
