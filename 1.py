from fl import fl
from requests_main import employer


def enter():
    input_data = str(input('Для создания справки по работодателю введите "1" \n '
                           'Для создания справки по ФЛ введите "2": 1'))
    if input_data == "1":
        employer()
    if input_data == "2":
        fl()


enter()

