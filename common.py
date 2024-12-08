# Импорт библиотек
#from calendar import month
from pickle import FALSE, TRUE
#import sys
# Подключаем модуль для работы с датой/временем
from datetime import datetime
from datetime import timedelta
# Подключаем модуль генерации случайных чисел
import random

# Получение случайной даты в заданном диапазоне дат
#start_dt = datetime.strptime("01.01.1963", "%d.%m.%Y")
#end_dt = datetime.strptime("01.01.2001", "%d.%m.%Y")
#print(get_random_date(start_dt, end_dt))
def get_random_date(start, end):
    delta = end - start
    return start + timedelta(random.randint(0, delta.days))

# Получение случайного адреса (k - включает ли адрес квартиру)
def get_adres(k):
    ulica = ["ул. Баженова", 
            "ул. Вавилова", 
            "ул. Гастелло", 
            "ул. Дружбы", 
            "ул. Защитная", 
            "ул. Ипподромная", 
            "ул. Кирпичная", 
            "ул. Луначарского", 
            "ул. Новоселов",
            "ул. Олимпийская", 
            "ул. Победы", 
            "ул. Университетская", 
            "ул. Фрунзе" 
        ]
    if (k==TRUE):
        adres = random.choice(ulica) + ", " + str(random.randint(1, 200)) + "-" + str(random.randint(1, 200)) 
    else:
        adres = random.choice(ulica) + ", " + str(random.randint(1, 200)) 
    return adres

# Получение случайного адреса (k - включает ли адрес квартиру)
def get_telefon():
    if random.randint(0, 1) == 1:
        telefon = "+7-910-"
    else:
        telefon = "+7-903-" 
    telefon = telefon + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + "-" + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) 
    return telefon
