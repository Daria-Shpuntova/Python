# -*- coding: utf-8 -*-
import requests
from requests.exceptions import ConnectionError
from time import sleep
import json
import pandas as pd

# Метод для корректной обработки строк в кодировке UTF-8 как в Python 3, так и в Python 2
import sys
import gspread as gs
import os
import random

# проверка версии пайтона
if sys.version_info < (3,):
    def u(x):
        try:
            return x.encode("utf8")
        except UnicodeDecodeError:
            return x
else:
    def u(x):
        if type(x) == type(b''):
            return x.decode('utf8')
        else:
            return x

# Адрес сервиса Reports для отправки JSON-запросов (регистрозависимый)
ReportsURL = 'https://api.direct.yandex.com/json/v5/reports'

# --- Входные данные ---

# OAuth-токен пользователя, от имени которого будут выполняться запросы
token = '#'

# Логин клиента рекламного агентства
# Обязательный параметр, если запросы выполняются от имени рекламного агентства
clientLogin = '#'

# какие столбцы подгрузить
stolbec = ['Month', 'CampaignName', 'Clicks', 'Cost', 'Conversions', 'AdGroupName', 'Age', 'Gender', "Device"]

# ID цели в Метрике
goalID = ['#']

# даты отчета
firstDate = "2023-01-01"
secondDate = "2023-04-25"

# назначаю файлик с данными моего аккаунта
accountData = gs.service_account(filename='custom-woodland-384917-41109128e58c.json')

# открываем Sheet
sh = accountData.open('test API')

# --- Подготовка запроса ---
# Создание HTTP-заголовков запроса
headers = {
    # OAuth-токен. Использование слова Bearer обязательно
    "Authorization": "Bearer " + token,
    # Логин клиента рекламного агентства
    "Client-Login": clientLogin,
    # Язык ответных сообщений
    "Accept-Language": "ru",
    # Режим формирования отчета
    "processingMode": "auto",
    # Формат денежных значений в отчете
    "returnMoneyInMicros": "false",
    # Не выводить в отчете строку с названием отчета и диапазоном дат
    # "skipReportHeader": "true",
    # Не выводить в отчете строку с названиями полей
    # "skipColumnHeader": "true",
    # Не выводить в отчете строку с количеством строк статистики
    "skipReportSummary": "true"
}

reportNumber = random.randrange(1, 200)

# Создание тела запроса
body = {
    "params": {
        "SelectionCriteria": {
            "DateFrom": firstDate,
            "DateTo": secondDate
        },
        "Goals": goalID,
        "FieldNames": stolbec,
        "ReportName": f'Отчет №{reportNumber}',
        "ReportType": "CRITERIA_PERFORMANCE_REPORT",
        "DateRangeType": "CUSTOM_DATE",
        "Format": "TSV",
        "IncludeVAT": "YES",
        "IncludeDiscount": "NO"
    }
}

# Кодирование тела запроса в JSON
body = json.dumps(body, indent=4)

# --- Запуск цикла для выполнения запросов ---
# Если получен HTTP-код 200, то выводится содержание отчета
# Если получен HTTP-код 201 или 202, выполняются повторные запросы
while True:
    try:
        req = requests.post(ReportsURL, body, headers=headers)

        req.encoding = 'utf-8'  # Принудительная обработка ответа в кодировке UTF-8
        if req.status_code == 400:
            print("Параметры запроса указаны неверно или достигнут лимит отчетов в очереди")
            print("RequestId: {}".format(req.headers.get("RequestId", False)))
            print("JSON-код запроса: {}".format(u(body)))
            print("JSON-код ответа сервера: \n{}".format(u(req.json())))
            break
        elif req.status_code == 200:
            print("Отчет создан успешно")
            print("RequestId: {}".format(req.headers.get("RequestId", False)))
            break
        elif req.status_code == 201:
            print("Отчет успешно поставлен в очередь в режиме офлайн")
            retryIn = int(20)
            print("Повторная отправка запроса через {} секунд".format(retryIn))
            print("RequestId: {}".format(req.headers.get("RequestId", False)))
            sleep(retryIn)
        elif req.status_code == 202:
            print("Отчет формируется в режиме офлайн")
            retryIn = int(req.headers.get("retryIn", 60))
            print("Повторная отправка запроса через {} секунд".format(retryIn))
            print("RequestId:  {}".format(req.headers.get("RequestId", False)))
            sleep(retryIn)
        elif req.status_code == 500:
            print("При формировании отчета произошла ошибка. Пожалуйста, попробуйте повторить запрос позднее")
            print("RequestId: {}".format(req.headers.get("RequestId", False)))
            print("JSON-код ответа сервера: \n{}".format(u(req.json())))
            break
        elif req.status_code == 502:
            print("Время формирования отчета превысило серверное ограничение.")
            print(
                "Пожалуйста, попробуйте изменить параметры запроса - уменьшить период и количество запрашиваемых данных.")
            print("JSON-код запроса: {}".format(body))
            print("RequestId: {}".format(req.headers.get("RequestId", False)))
            print("JSON-код ответа сервера: \n{}".format(u(req.json())))
            break
        else:
            print("Произошла непредвиденная ошибка")
            print("RequestId:  {}".format(req.headers.get("RequestId", False)))
            print("JSON-код запроса: {}".format(body))
            print("JSON-код ответа сервера: \n{}".format(u(req.json())))
            break

    # Обработка ошибки, если не удалось соединиться с сервером API Директа
    except ConnectionError:
        # В данном случае мы рекомендуем повторить запрос позднее
        print("Произошла ошибка соединения с сервером API")
        # Принудительный выход из цикла
        break

    # Если возникла какая-либо другая ошибка
    except:
        # В данном случае мы рекомендуем проанализировать действия приложения
        print("Произошла непредвиденная ошибка")
        # Принудительный выход из цикла
        break

# создаем csv файл и записываем в него ответ
file = open("cashe.csv", "w", encoding='utf-8')
file.write(req.text)
file.close()

# проверяем кодировку файла и если ошибка - применяем UTF-8
df = pd.read_csv("cashe.csv", header=1, sep='\t', encoding="utf-8")

# меняем значения в конверсиях - на 0, переводит в int

for col in df.columns:
    if 'Conversions' in col:
        df[col] = df[col].replace('--', '0').astype(int)
        conv = col

# меняем вид возраста
if "Age" in stolbec:
    df['Age'] = df['Age'].replace(to_replace=r'AGE_', value='Возраст ', regex=True).replace(to_replace=r'_', value='-',
                                                                                            regex=True)

# меняем вид пола
if "Gender" in stolbec:
    df['Gender'] = df['Gender'].replace(to_replace=r'GENDER_MALE', value='Мужчины', regex=True).replace(
        to_replace=r'GENDER_FEMALE', value='Женщины', regex=True)

# меняем значения в устройствах
if 'Device' in stolbec:
    df['Device'] = df['Device'].replace(to_replace=r'DESKTOP', value='Компьтер', regex=True).replace(
        to_replace=r'TABLET', value='Планшет', regex=True).replace(to_replace=r'MOBILE', value='Мобильный', regex=True)

# заполняем пустые ячейки
df.fillna('', inplace=True)

worksheet = sh.get_worksheet(0)  # открываем WS

worksheet.clear()  # чистим таблицу

cols = df.columns.values.tolist()  # названия в столбик

rows = df.values.tolist()  # строки, построчно

worksheet.update([cols] + rows)  # заливаем в таблицу

