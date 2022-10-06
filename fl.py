from passwords import token_ofdata
import requests
from docxtpl import DocxTemplate


def zapros(inn):
    url = f'https://api.ofdata.ru/v2/person?key={token_ofdata}&inn={inn}'
    response = requests.get(url).json()
    print(response['meta'])
    return response

def founders(json_f):
    founder_current = []
    founder_liquidated = []
    for org in json_f['data']['Учред']:
        if "Действует" in org['Статус']:
            name = org['НаимСокр']
            inn = org['ИНН']
            ogrn = org['ОГРН']
            okved = org['ОКВЭД']
            adress = org['ЮрАдрес']
            founder_current.append(f'{name} \n {okved} \n участник -    % в УК'
                                   f' \n ИНН: {inn} ОГРН: {ogrn}')
        else:
            name = org['НаимСокр']
            inn = org['ИНН']
            ogrn = org['ОГРН']
            okved = org['ОКВЭД']
            adress = org['ЮрАдрес']
            date_likv = org['ДатаЛикв']
            founder_liquidated.append(
                f'{name} \n {okved} \n ИНН: {inn} ОГРН: {ogrn} \n '
                f'Дата ликвидации - {date_likv}')
    my_dict = {'founder_current':"\n".join(founder_current),
               'founder_liquidated': "\n".join(founder_liquidated)}
    return my_dict

def managers (json_f):
    manager_current = []
    manager_liquidated = []
    for org in json_f['data']['Руковод']:
        if "Действует" in org['Статус']:
            name = org['НаимСокр']
            inn = org['ИНН']
            ogrn = org['ОГРН']
            okved = org['ОКВЭД']
            adress = org['ЮрАдрес']
            manager_current.append(f'{name} \n {okved} \n ИНН: {inn} ОГРН: {ogrn}')
        else:
            name = org['НаимСокр']
            inn = org['ИНН']
            ogrn = org['ОГРН']
            okved = org['ОКВЭД']
            adress = org['ЮрАдрес']
            # date_likv = org['ДатаЛикв']
            manager_liquidated.append(
                f'{name} \n {okved} \n ИНН: {inn} ОГРН: {ogrn} \n '
                f'Дата ликвидации - ')
    my_dict = {'manager_current':"\n".join(manager_current),
               'manager_liquidated': "\n".join(manager_liquidated)}
    return my_dict

def businessman(json_f):
    businessman_current = []
    businessman_liquidated = []
    for org in json_f['data']['ИП']:
        if "Действующий" in org['Статус']:
            name = org['ФИО']
            inn = org['ИНН']
            ogrn = org['ОГРНИП']
            okved = org['ОКВЭД']
            type = org['Тип']
            date_reg = org['ДатаРег']
            businessman_current.append(f'{type} {name} \n {okved} \n '
                                       f'ИНН: {inn} ОГРНИП: {ogrn} \n '
                                       f'Дата регистрации: {date_reg}')
        if "Недействующий" in org['Статус']:
            name = org['ФИО']
            inn = org['ИНН']
            ogrn = org['ОГРНИП']
            okved = org['ОКВЭД']
            type = org['Тип']
            date_reg = org['ДатаРег']
            date_liq = org['ДатаПрекращ']
            businessman_liquidated.append(f'{type} {name} \n {okved} \n'
                                          f' ИНН: {inn} ОГРНИП: {ogrn} \n'
                                          f' Дата регистрации: {date_reg} \n'
                                          f' Дата прекращения: {date_liq}')
    my_dict = {'businessman_current':"\n".join(businessman_current),
               'businessman_liquidated': "\n".join(businessman_liquidated)}
    return my_dict

def union_dict(dict_1, dict_2, dict_3):
    union_dict = dict_1|dict_2|dict_3
    return union_dict

def word_founders(my_dict):
    doc = DocxTemplate("founders.docx")
    context = my_dict
    doc.render(context)
    doc.save('Запрос по ИНН ФЛ.docx')

def fl():
    inn_fl = str(input("Введите ИНН физического лица: "))
    res = zapros(inn_fl)
    founder = founders(res)
    manager = managers(res)
    busines = businessman(res)
    union_data = union_dict(founder, manager, busines)
    word_founders(union_data)

fl()
