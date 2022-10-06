from passwords import token_ofdata
import requests
from docxtpl import DocxTemplate
from datetime import datetime
from postmail import sendmail


def zapros(inn):
    inn = inn
    url = f'https://api.ofdata.ru/v2/company?key={token_ofdata}&inn={inn}'
    response = requests.get(url).json()
    print(response['meta'])
    return response


def data_requisites(json_f):
    inn = json_f['data']['ИНН']  # ИНН
    ogrn = json_f['data']['ОГРН']  # ОГРН
    date_reg = datetime.strptime(json_f['data']['ДатаРег'],
                                 '%Y-%m-%d')  # Дата регистрации
    full_name = json_f['data']['НаимПолн']  # Полное наименование
    abbreviated_name = json_f['data']['НаимСокр']  # Короткое наименование
    ifns = json_f['data']['РегФНС']['НаимОрг']  # Регистрирующий орган
    sole_executive_body = json_f['data']['Руковод'][0][
        'НаимДолжн']  # Наименование должности единоличного исполнительного органа
    fio_sole_executive_body = json_f['data']['Руковод'][0][
        'ФИО']  # ФИО единоличного исполнительного органа
    inn_sole_executive_body = json_f['data']['Руковод'][0][
        'ИНН']  # ИНН единоличного исполнительного органа
    legal_adress = json_f['data']['ЮрАдрес']['АдресРФ']  # Юридический адрес
    authorized_capital = json_f['data']['УстКап']['Сумма']  # Уставный капитал
    status = json_f['data']['Статус'][
        'Наим']  # Статус (действующее/не действующее)
    founders_list_text = []  # Учредители (поступают в список из циклов (с участием в иных организациях))
    founders_list_employer = []  # Учредители (поступают в список из циклов (без участия в иных организациях))
    size = json_f['data']['СЧР']  # Среднесписочная численность
    okved_name = json_f['data']['ОКВЭД']['Наим']  # ОКВЭД текст
    okved_code = json_f['data']['ОКВЭД']['Код']  # ОКВЭД код
    nalogs = json_f['data'][
        'Налоги']  # Налоги (возвращает словарь, надо рабираться)
    license = json_f['data'][
        'Лиценз']  # Лицензии (возвращает словарь, надо рабираться)
    mass_manager = json_f['data'][
        'МассРуковод']  # Признак присутствия массовых руководителей
    mass_founder = json_f['data'][
        'МассУчред']  # Признак присутствия массовых учредителей
    unscrupulous_supplier = json_f['data'][
        'НедобПост']  # Проверка по реестру недобросовестных поставщиков
    disqualified_person = json_f['data'][
        'ДисквЛица']  # Признак присутствия дисквалифицированных лиц в руководстве компании
    divisions = json_f['data'][
        'Подразд']  # Подразделения (возвращает словарь, надо рабираться)
    rmsp = json_f['data'][
        'РМСП']  # Информация о включении в Единый реестр субъектов малого и среднего предпринимательства (возвращает словарь, надо рабираться)
    permission = []  # Список лицензий
    filials = []  # Список филиалов
    preds = []  # Список представительств
    nalogs_list = []  # список налогов
    for founder_ul in json_f['data']['Учред']['РосОрг']:  # Учредитель ЮЛ
        try:
            name_founder = founder_ul['НаимПолн']
            ogrn_founder = founder_ul['ОГРН']
            inn_founder = founder_ul['ИНН']
            fraction_money = founder_ul['Доля']['Номинал']
            fraction_percent = founder_ul['Доля']['Процент']
            founders_list_employer.append(f'- {name_founder}, ИНН {inn_founder} - '
                                        f'{fraction_percent}% в УК ({fraction_money}'
                                        f' рублей)\n')
        except:
            founders_list_employer.append('Что-то пошло не так')
    for founder in json_f['data']['Учред']['ФЛ']:  # Учредитель ФЛ
        fio_founder = founder['ФИО']
        inn_founder = founder['ИНН']
        fraction_money = founder['Доля']['Номинал']
        fraction_percent = founder['Доля']['Процент']
        communication_by_supervisor = founder['СвязРуковод']
        communication_by_founder = founder['СвязУчред']
        founders_list_text.append(
            f'- {fio_founder}, ИНН {inn_founder} - {fraction_percent}% '
            f'в УК ({fraction_money} рублей)\n принимает участие в'
            f' следующих организациях:\n - в качестве руководителя: '
            f'{communication_by_supervisor};\n - в качестве учредителя:'
            f'{communication_by_founder}')
        founders_list_employer.append(
            f'- {fio_founder}, ИНН {inn_founder} - {fraction_percent}% '
            f'в УК ({fraction_money} рублей)')
    for founder_foreigner in json_f['data']['Учред'][
        'ИнОрг']:  # Учредитель нерезидент
        name_founder = founder_foreigner['НаимПолн']
        grn_founder = founder_foreigner['РегНомер']
        fraction_money = founder_foreigner['Доля']['Номинал']
        fraction_percent = founder_foreigner['Доля']['Процент']
        country = founder_foreigner['Страна']
        founders_list_employer.append(f'- {name_founder}, рег.№ {grn_founder}, '
                                    f'{country} - {fraction_percent}%'
                                    f' в УК ({fraction_money} рублей)\n')
    if len(json_f['data']['Лиценз']) == 0:  # Лицензии
        permission.append('В ЕГРЮЛ отсутствуют сведения о выданных лицензиях')
    else:
        for lic in json_f['data']['Лиценз']:
            deyat = lic['ВидДеят']
            date = datetime.strptime(lic['Дата'], '%Y-%m-%d')
            org = lic['ЛицОрг']
            numb = lic['Номер']
            permission.append(
                f'- Лицензия № {numb} от {date.date().strftime("%d.%m.%Y")}'
                f' г.;\nВыдавший орган: {org.lower()}; '
                f'\nРазрешенные виды деятельности деятельности: {"; ".join(deyat)} ')
    if 'Филиал' in json_f['data']['Подразд']:  # Филиалы
        for filial in json_f['data']['Подразд']['Филиал']:
            fil_adress = filial['Адрес']
            fil_kpp = filial['КПП']
            fil_name = filial['НаимПолн']
            filials.append(
                f'{fil_name} (КПП: {fil_kpp}) \n расположен по адресу: {fil_adress}')
    if 'Представ' in json_f['data']['Подразд']:  # Представительства
        for z in json_f['data']['Подразд']['Представ']:
            preds_name = z['НаимПолн']
            preds_country = z['Страна']
            preds.append(f'{preds_name} (Страна: {preds_country})')
    else:
        filials.append(
            'Согласно сведениям ЕГРЮЛ организация не имеет филиалов')

    if 'Ликвид' in json_f['data']:  # Сведения о ликвидации
        date = datetime.strptime(json_f['data']['Ликвид']['Дата'], '%Y-%m-%d')
        reason = json_f['data']['Ликвид']['Наим']
        reason_date = f'{reason} - {date.date().strftime("%d.%m.%Y")}'
    else:
        reason_date = 'Сведения о ликвидации отсутствуют'
    if 'СведУпл' in json_f['data']['Налоги']:
        for nalog in json_f['data']['Налоги']['СведУпл']:
            nalog_name = nalog['Наим']
            nalog_sum = nalog['Сумма']
            nalogs_list.append(f'{nalog_name} - {nalog_sum} рублей;\n')
    else:
        nalogs_list.append('сведения отсутствуют')
    employer_dict = {'full_name': full_name,
                     'short_name': abbreviated_name,
                     'inn': inn,
                     'ogrn': ogrn,
                     'General_manager': f'{sole_executive_body.capitalize()} {fio_sole_executive_body}, '
                                        f'ИНН: {inn_sole_executive_body}',
                     'Founders': "\n".join(founders_list_employer),
                     'date_of_registration': date_reg.date().strftime(
                         '%d.%m.%Y'),
                     'Legal_address': legal_adress,
                     'authorized_capital': authorized_capital,
                     'okved': okved_name,
                     'size': size,
                     'permission': "\n".join(permission),
                     'filials': "\n".join(filials),
                     'preds': "\n".join(preds),
                     'status': status.upper(),
                     'reason_date': reason_date.lower(),
                     'nalogs': "\n".join(nalogs_list)}
    return employer_dict


def word_employer(my_dict):
    doc = DocxTemplate("employer.docx")
    context = my_dict
    doc.render(context)
    short_name = my_dict["short_name"].replace('"', '')
    date = datetime.now().date().strftime('%d.%m.%Y')
    file_name = f"{short_name}_{date}.docx"
    doc.save(file_name)
    return file_name


def employer():
    inn_org = str(input("Введите ИНН: "))
    sendmail(word_employer(data_requisites(zapros(inn_org))))


employer()
