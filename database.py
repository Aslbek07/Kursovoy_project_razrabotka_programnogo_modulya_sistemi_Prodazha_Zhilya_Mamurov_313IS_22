# Импорт библиотек
from pickle import FALSE, TRUE
import sys
# Подключаем модуль для SQLite
import sqlite3
# Подключаем модуль для работы с датой/временем
from datetime import datetime, timedelta
# Поделючаем модкль генерации случайных чисел
import random
# Подключаем модуль для создания подключения к БД
import connector
# Подключаем общий для всего проекта модуль
import common
# Модуль hashlib реализует общий интерфейс для множества различных безопасных алгоритмов хеширования и дайджеста сообщений
import hashlib
# Модуль os предоставляет множество функций для работы с операционной системой, причём их поведение, как правило, не зависит от ОС, поэтому программы остаются переносимыми. 
import os


# Создание базы данных, заполнение ее начальными данными 
def init_db():
    try:
        # Подключение к SQLite 
        # Вызов функции connect() приводит к созданию объекта-экземпляра от класса Connection.
        # Этот объект обеспечивает связь с файлом базы данных, представляет конкретную БД в программе                             
        conn = connector.get_connection()
        print("База данных SQLite подключена")
        # Объект cursor, позволяет взаимодействовать с базой данных             
        cursor = conn.cursor()

        ######################
        ##### polzovatel #####
        ######################

        # Проверка наличия таблицы 
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='polzovatel'")
        result = cursor.fetchall()
        if len(result) > 0:
            print("Таблица polzovatel уже существует")        
        else:
            print("Создается таблица polzovatel")  
            create_table_query = '''CREATE TABLE polzovatel (
                                id INTEGER NOT NULL,                                
                                login VARCHAR(128) NOT NULL UNIQUE,
                                parol VARCHAR(256) NOT NULL,
                                administrator BOOL,
                                menedzher BOOL,
                                PRIMARY KEY("id" AUTOINCREMENT));'''
            # Выполнение команды: это создает новую таблицу
            cursor.execute(create_table_query)
            conn.commit()
            print("Таблица polzovatel создана")        
        # Заполнение таблицы (один раз)
        sql = "SELECT id FROM polzovatel"
        # С помощью метода execute объекта cursor можно выполнить запрос в базу данных из Python.
        # Он принимает SQL-запрос в качестве параметра и возвращает resultSet (строки базы данных):
        cursor.execute(sql)
        # Получить результат запроса из resultSet можно с помощью методов, например, fetchAll()
        row = cursor.fetchone()
        # Если таблица пустая - заполнить ее
        if row is None:
            cursor.execute("INSERT INTO polzovatel VALUES (Null, 'admin', '" + hashlib.sha256("admin".encode('utf-8')).hexdigest() + "', 1, 0)")
            cursor.execute("INSERT INTO polzovatel VALUES (Null, 'manager', '" + hashlib.sha256("manager".encode('utf-8')).hexdigest() + "', 0, 1)")
            cursor.execute("INSERT INTO polzovatel VALUES (Null, 'user', '" + hashlib.sha256("user".encode('utf-8')).hexdigest() + "', 0, 0)")
            conn.commit()
            print("Таблицы polzovatel заполнена")       

        #####################
        ##### dolzhnost #####
        #####################

        # Проверка наличия таблицы 
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='dolzhnost'")
        result = cursor.fetchall()
        if len(result) > 0:
            print("Таблица dolzhnost уже существует")        
        else:
            print("Создается таблица dolzhnost")  
            create_table_query = '''CREATE TABLE dolzhnost (
                                id INTEGER NOT NULL,                                
                                nazvanie VARCHAR(128) NOT NULL UNIQUE,
                                PRIMARY KEY("id" AUTOINCREMENT));'''
            # Выполнение команды: это создает новую таблицу
            cursor.execute(create_table_query)
            conn.commit()
            print("Таблица dolzhnost создана")        
        # Заполнение таблицы (один раз)
        sql = "SELECT id FROM dolzhnost"
        # С помощью метода execute объекта cursor можно выполнить запрос в базу данных из Python.
        # Он принимает SQL-запрос в качестве параметра и возвращает resultSet (строки базы данных):
        cursor.execute(sql)
        # Получить результат запроса из resultSet можно с помощью методов, например, fetchAll()
        row = cursor.fetchone()
        # Если таблица пустая - заполнить ее
        if row is None:
            cursor.execute("INSERT INTO dolzhnost VALUES (Null, 'Директор агентства')")
            cursor.execute("INSERT INTO dolzhnost VALUES (Null, 'Старший агент по недвижимости')")
            cursor.execute("INSERT INTO dolzhnost VALUES (Null, 'Агент по недвижимости')")
            conn.commit()
            print("Таблицы dolzhnost заполнена")     
   
        #####################
        ##### sotrudnik #####
        #####################

        # Проверка наличия таблицы 
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sotrudnik'")
        result = cursor.fetchall()
        if len(result) > 0:
            print("Таблица sotrudnik уже существует")        
        else:
            print("Создается таблица sotrudnik")  
            create_table_query = '''CREATE TABLE sotrudnik (
                                id INTEGER NOT NULL,                                
                                fio VARCHAR(128) NOT NULL,
                                adres VARCHAR(96) NOT NULL,
                                telefon VARCHAR(64) NOT NULL,
                                dolzhnost_id INTEGER NOT NULL,
                                PRIMARY KEY("id" AUTOINCREMENT),
                                FOREIGN KEY("dolzhnost_id") REFERENCES "dolzhnost"("id") ON DELETE CASCADE);'''
            # Выполнение команды: это создает новую таблицу
            cursor.execute(create_table_query)
            conn.commit()
            print("Таблица sotrudnik создана")        
        # Заполнение таблицы (один раз)
        sql = "SELECT id FROM sotrudnik"
        # С помощью метода execute объекта cursor можно выполнить запрос в базу данных из Python.
        # Он принимает SQL-запрос в качестве параметра и возвращает resultSet (строки базы данных):
        cursor.execute(sql)
        # Получить результат запроса из resultSet можно с помощью методов, например, fetchAll()
        row = cursor.fetchone()
        # Если таблица пустая - заполнить ее
        if row is None:
            # Текущая папка
            current_directory = os.getcwd()
            # SQL запрос
            sql = "INSERT INTO sotrudnik (fio, adres, telefon, dolzhnost_id) VALUES (?, ?, ?, ?)"
            # Параметры запроса, выполнение запроса
            parameters = ['Кожанов Владимир Сергеевич', common.get_adres(TRUE), common.get_telefon(), 1]            
            cursor.execute(sql, parameters)
            parameters = ['Ермолина Ирина Викторовна', common.get_adres(TRUE), common.get_telefon(), 2]            
            cursor.execute(sql, parameters)
            parameters = ['Томилов Игорь Дмитриевич', common.get_adres(TRUE), common.get_telefon(), 2]            
            cursor.execute(sql, parameters)
            parameters = ['Данилов Александр Андреевич', common.get_adres(TRUE), common.get_telefon(), 3]            
            cursor.execute(sql, parameters)
            parameters = ['Пан Данил Евгеньевич', common.get_adres(TRUE), common.get_telefon(), 3]            
            cursor.execute(sql, parameters)
            parameters = ['Юрченко Сабина Юрьевна', common.get_adres(TRUE), common.get_telefon(), 3]            
            cursor.execute(sql, parameters)
            parameters = ['Виниченко Екатерина Евгеньевна', common.get_adres(TRUE), common.get_telefon(), 3]            
            cursor.execute(sql, parameters)
            parameters = ['Крапивина Алёна Витальевна', common.get_adres(TRUE), common.get_telefon(), 3]            
            cursor.execute(sql, parameters)
            parameters = ['Коломиец Анна Алексеевна', common.get_adres(TRUE), common.get_telefon(), 3]            
            cursor.execute(sql, parameters)
            parameters = ['Панин Виктор Романович', common.get_adres(TRUE), common.get_telefon(), 3]            
            cursor.execute(sql, parameters)

        ##########################
        ##### view_sotrudnik #####
        ##########################

        # Проверка наличия представления 
        cursor.execute("SELECT name FROM sqlite_master WHERE type='view' AND name='view_sotrudnik'")
        result = cursor.fetchall()
        if len(result) > 0:
            print("Представление view_sotrudnik уже существует")        
        else:
            print("Создается представление view_sotrudnik")  
            create_table_query = '''CREATE VIEW view_sotrudnik AS
                SELECT sotrudnik.id, sotrudnik.fio, sotrudnik.adres, sotrudnik.telefon, sotrudnik.dolzhnost_id, dolzhnost.nazvanie AS dolzhnost 
                    FROM sotrudnik LEFT JOIN dolzhnost ON sotrudnik.dolzhnost_id = dolzhnost.id;'''
            # Выполнение команды: это создает новую таблицу
            cursor.execute(create_table_query)
            conn.commit()
            print("Представление view_sotrudnik создано")      
            
        ##################
        ##### klient #####
        ##################

        # Проверка наличия таблицы 
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='klient'")
        result = cursor.fetchall()
        if len(result) > 0:
            print("Таблица klient уже существует")        
        else:
            print("Создается таблица klient")  
            create_table_query = '''CREATE TABLE klient (
                                id INTEGER NOT NULL,                                
                                fio VARCHAR(128) NOT NULL,
                                adres VARCHAR(96) NOT NULL,
                                telefon VARCHAR(64) NOT NULL,
                                PRIMARY KEY("id" AUTOINCREMENT));'''
            # Выполнение команды: это создает новую таблицу
            cursor.execute(create_table_query)
            conn.commit()
            print("Таблица klient создана")        
        # Заполнение таблицы (один раз)
        sql = "SELECT id FROM klient"
        # С помощью метода execute объекта cursor можно выполнить запрос в базу данных из Python.
        # Он принимает SQL-запрос в качестве параметра и возвращает resultSet (строки базы данных):
        cursor.execute(sql)
        # Получить результат запроса из resultSet можно с помощью методов, например, fetchAll()
        row = cursor.fetchone()
        # Если таблица пустая - заполнить ее
        if row is None:
            # Текущая папка
            current_directory = os.getcwd()
            
            # SQL запрос
            sql = "INSERT INTO klient (fio, adres, telefon) VALUES (?, ?, ?)"
            # Параметры запроса, выполнение запроса
            parameters = ['Бирюлин Рустам Валерьевич', common.get_adres(TRUE), common.get_telefon()]
            cursor.execute(sql, parameters)
            parameters = ['Сиваш Алексей Владимирович', common.get_adres(TRUE), common.get_telefon()]
            cursor.execute(sql, parameters)
            parameters = ['Лосева Дарья Борисовна', common.get_adres(TRUE), common.get_telefon()]
            cursor.execute(sql, parameters)
            parameters = ['Кобзев Дмитрий Александрович', common.get_adres(TRUE), common.get_telefon()]
            cursor.execute(sql, parameters)
            parameters = ['Яцковский Илья Юрьевич', common.get_adres(TRUE), common.get_telefon()]
            cursor.execute(sql, parameters)
            parameters = ['Лобкарев Сергей Андреевич', common.get_adres(TRUE), common.get_telefon()]
            cursor.execute(sql, parameters)
            parameters = ['Сорока Андрей Андреевич', common.get_adres(TRUE), common.get_telefon()]
            cursor.execute(sql, parameters)
            parameters = ['Гончарова Елена Андреевна', common.get_adres(TRUE), common.get_telefon()]
            cursor.execute(sql, parameters)
            parameters = ['Гроссул Павел Павлович', common.get_adres(TRUE), common.get_telefon()]
            cursor.execute(sql, parameters)
            parameters = ['Машуков Артём Андреевич', common.get_adres(TRUE), common.get_telefon()]
            cursor.execute(sql, parameters)
            parameters = ['Филиоглова Наталья Александровна', common.get_adres(TRUE), common.get_telefon()]
            cursor.execute(sql, parameters)
            parameters = ['Овсянников Станислав Валерьевич', common.get_adres(TRUE), common.get_telefon()]
            cursor.execute(sql, parameters)
            parameters = ['Авдеева Екатерина Викторовна', common.get_adres(TRUE), common.get_telefon()]
            cursor.execute(sql, parameters)
            parameters = ['Воробьев Дмитрий Михайлович', common.get_adres(TRUE), common.get_telefon()]
            cursor.execute(sql, parameters)
            parameters = ['Бабич Сергей Сергеевич', common.get_adres(TRUE), common.get_telefon()]
            cursor.execute(sql, parameters)
            parameters = ['Алексеенко Екатерина Константиновна', common.get_adres(TRUE), common.get_telefon()]
            cursor.execute(sql, parameters)
            parameters = ['Казаковцев Николай Алексеевич', common.get_adres(TRUE), common.get_telefon()]
            cursor.execute(sql, parameters)
            parameters = ['Вохмяков Владислав Сергеевич', common.get_adres(TRUE), common.get_telefon()]
            cursor.execute(sql, parameters)
            parameters = ['Верзакова Валерия Владиславовна', common.get_adres(TRUE), common.get_telefon()]
            cursor.execute(sql, parameters)
            parameters = ['Степанов Станислав Михаилович', common.get_adres(TRUE), common.get_telefon()]
            cursor.execute(sql, parameters)
                    
        ################
        ##### tip #####
        ################

        # Проверка наличия таблицы 
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tip'")
        result = cursor.fetchall()
        if len(result) > 0:
            print("Таблица tip уже существует")        
        else:
            print("Создается таблица tip")  
            create_table_query = '''CREATE TABLE tip (
                                id INTEGER NOT NULL,                                
                                nazvanie VARCHAR(128) NOT NULL UNIQUE,
                                PRIMARY KEY("id" AUTOINCREMENT));'''
            # Выполнение команды: это создает новую таблицу
            cursor.execute(create_table_query)
            conn.commit()
            print("Таблица tip создана")        
        # Заполнение таблицы (один раз)
        sql = "SELECT id FROM tip"
        # С помощью метода execute объекта cursor можно выполнить запрос в базу данных из Python.
        # Он принимает SQL-запрос в качестве параметра и возвращает resultSet (строки базы данных):
        cursor.execute(sql)
        # Получить результат запроса из resultSet можно с помощью методов, например, fetchAll()
        row = cursor.fetchone()
        # Если таблица пустая - заполнить ее
        if row is None:
            cursor.execute("INSERT INTO tip VALUES (Null, 'Квартира')")
            cursor.execute("INSERT INTO tip VALUES (Null, 'Жилой дом')")
            cursor.execute("INSERT INTO tip VALUES (Null, 'Комната в общежитии')")
            conn.commit()
            print("Таблицы tip заполнена")  

        #################
        ##### zhile #####
        #################

        # Проверка наличия таблицы 
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='zhile'")
        result = cursor.fetchall()
        if len(result) > 0:
            print("Таблица zhile уже существует")        
        else:
            print("Создается таблица zhile")  
            create_table_query = '''CREATE TABLE zhile (
                                id INTEGER NOT NULL,       
								tip_id INTEGER NOT NULL,								
								komnata INTEGER NOT NULL,								
                                adres VARCHAR(128) NOT NULL,
								polshchad1 INTEGER NOT NULL,								
								polshchad2 INTEGER NOT NULL,								
								etazh INTEGER NOT NULL,								
								etazhnost INTEGER NOT NULL,								
                                opisanie TEXT NOT NULL,
                                data DATETIME NOT NULL,
                                price DECIMAL NOT NULL,
                                klient_id INTEGER NOT NULL,
                                aktiv BOOL,
                                PRIMARY KEY("id" AUTOINCREMENT),
                                FOREIGN KEY("tip_id") REFERENCES "tip"("id") ON DELETE CASCADE,
                                FOREIGN KEY("klient_id") REFERENCES "klient"("id") ON DELETE CASCADE);'''
            # Выполнение команды: это создает новую таблицу
            cursor.execute(create_table_query)
            conn.commit()
            print("Таблица zhile создана")        
        # Заполнение таблицы (один раз)
        sql = "SELECT id FROM zhile"
        # С помощью метода execute объекта cursor можно выполнить запрос в базу данных из Python.
        # Он принимает SQL-запрос в качестве параметра и возвращает resultSet (строки базы данных):
        cursor.execute(sql)
        # Получить результат запроса из resultSet можно с помощью методов, например, fetchAll()
        row = cursor.fetchone()
        # Если таблица пустая - заполнить ее
        if row is None:
            sql = "INSERT INTO zhile (tip_id, komnata, adres, polshchad1, polshchad2, etazh, etazhnost, opisanie, data, price, klient_id, aktiv) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            # Параметры запроса, Выполнение запроса
            d = datetime.now().date() - timedelta(days=28)
            parameters = [1, 1, common.get_adres(FALSE), 41, 11, 20, 24, "Пpодаю ВИДOВУЮ классичеcкую однoкомнaтную квартиpу в нoвoм 2023 года пocтpoйки мoнолитном домe. Из oкон oткрывается пaнорaмный вид нa Mocкву!", d, 1270000, 1,  0]
            cursor.execute(sql, parameters)
            d = datetime.now().date() - timedelta(days=28)
            parameters = [1, 1, common.get_adres(FALSE), 44, 20, 33, 33, "ТOПовaя ВИДОВAЯ квартира в Hовoм сдaнoм в 2022 гoду домe нeбоcкpeбe!", d, 9500000, 2,  1]
            cursor.execute(sql, parameters)
            d = datetime.now().date() - timedelta(days=28)
            parameters = [1, 1, common.get_adres(FALSE), 39, 9, 1, 14, "Идeaльный вариант для инвecтиций: 1 к.кв-ра с качеcтвенным pемонтoм! Гoтoвая квартирa кaк для coбcтвенного пpoживания, тaк и для сдачи в арeнду.", d, 8900000, 3,  1]
            cursor.execute(sql, parameters)
            d = datetime.now().date() - timedelta(days=27)
            parameters = [1, 1, common.get_adres(FALSE), 36, 8, 3, 5, "Пpодается уютная однoкомнaтная квартирa в ЦАO. Дом кирпичный, ж/б пepeкpытия. Уxоженный подъeзд.", d, 13600000, 4,  1]
            cursor.execute(sql, parameters)
            d = datetime.now().date() - timedelta(days=27)
            parameters = [1, 1, common.get_adres(FALSE), 38, 12, 9, 20, "КBAРТИРА oдна изoлирoваннaя кoмнaта, куxня гocтинaя, гapдeробная, coвмещeнный санузел, и приxожая.", d, 22500000, 5,  0]
            cursor.execute(sql, parameters)
            d = datetime.now().date() - timedelta(days=27)
            parameters = [1, 2, common.get_adres(FALSE), 54, 10, 1, 5, "Вoзможен нeбольшой торг! С предлoжениями пpиобpecти зa 10-11 oтправляю cpaзу в блoк, бepите доли, либо учacтвуйте в aукционах, подoбных прeдлoжeний зa эту цeну по всей Moскве внутри MKАД нe найти, почему?! Дочитaйтe до концa!😉Hе aгенcтвo, собствeнник! Отдaю по цeнe oднушки двушку с бoльшим метpaжем, прoдуманной плaнировкой и все это в 6 км от центра внутри МКАД, в перспективном и престижном районе на севере Москвы. ", d, 11900000, 6,  1]            
            cursor.execute(sql, parameters)
            d = datetime.now().date() - timedelta(days=26)
            parameters = [1, 2, common.get_adres(FALSE), 41, 14, 15, 22, "Eвро двушка! 42 м! 15 этаж - Самая Лучшaя и Видoвая! Kваpтирa в новом ЖК «Hacтpoение», отдeлкa Whitе Bох. Вид на нaциональный пapк Лocиный Oстров (лёгкиe Mосквы). Тeплaя, наxодиться внутри домa, нe Тоpцeвая!", d, 14500000, 7,  1]
            cursor.execute(sql, parameters)
            d = datetime.now().date() - timedelta(days=26)
            parameters = [1, 2, common.get_adres(FALSE), 45, 8, 7, 9, "Продаётcя сoврeмeнная квapтиpа. В квapтиpe никтo не жил послe pемoнта, все новoе! Делaли для ceбя.", d, 17500000, 8,  1]
            cursor.execute(sql, parameters)
            d = datetime.now().date() - timedelta(days=26)
            parameters = [1, 2, common.get_adres(FALSE), 47, 6, 4, 5, "Пpoдаю двухкoмнaтную квapтиру после pемoнта, вcё cделано «пoд сeбя». Meбeль и тexнику могу докупить под зaпpоc.", d, 17100000, 9,  0]
            cursor.execute(sql, parameters)
            d = datetime.now().date() - timedelta(days=25)
            parameters = [1, 2, common.get_adres(FALSE), 62, 14, 24, 25, "Kвaртиpа paсположeна в нoвoм домe, пocтрoeннoм в 2022 году. Киpпично-монолитный тип постройки гарантирует надёжность и долговечность дома. В квартире установлены железобетонные перекрытия, обеспечивающие высокую прочность здания.", d, 18550000, 10,  1]
            cursor.execute(sql, parameters)
            d = datetime.now().date() - timedelta(days=25)
            parameters = [1, 3, common.get_adres(FALSE), 80, 15, 11, 20, "Kвapтира без oтдeлки, два c/у, два балкона, фpанцузскиe oкнa в пoл, цeнтральноe кoндиционировaниe, круглoсуточная оxpана, cвoй подзeмный паpкинг, зaкрытая теpритoрия. Нa тeрритopии кoмплексa уже открываются различные уютные кафе, магазины, пекарни.", d, 35000000, 11,  1]
            cursor.execute(sql, parameters)
            d = datetime.now().date() - timedelta(days=25)
            parameters = [1, 3, common.get_adres(FALSE), 131, 13, 3, 25, "Пpоcтopнaя cветлая квартирa в ЖК «Hежинcкий кoвчeг» в caмoм зелёнoм paйoнe Mосквы. За жилым кoмплeксoм большая зелёная зaповеднaя зoнa, нaпpотив - яблоневый caд Анны Гермaн. Жилoй комплeкт с закрытой тepритоpиeй и подзeмным паpкингoм. На откpытой паpковкe pядом вceгдa eсть меcта, нет загруженности по утрам. Рядом с ЖК продуктовый магазин и аптека.", d, 50900000, 12,  1]            
            cursor.execute(sql, parameters)
            d = datetime.now().date() - timedelta(days=24)
            parameters = [1, 3, common.get_adres(FALSE), 79, 9, 4, 5, " Bсе окна квaртиры выxoдят вo двop, утопающий в зелeни. B доме прoвeден кaпитальный ремонт c утeплением cтeн, оcтеклeниeм балконов, зaменой всeх кoммуникаций. Кваpтиpа рaсположена на 4 этаже. В квартире 6 окон, 2 застекленных балкона со шкафами для хранения вещей. В квартире сделан дизайнерский ремонт. Сделаны большие встроенные зеркальные шкафы в коридоре, гостиной. ", d, 28200000, 13,  0]
            cursor.execute(sql, parameters)
            d = datetime.now().date() - timedelta(days=24)
            parameters = [1, 3, common.get_adres(FALSE), 69, 7, 5, 9, "Bашему внимaнию пpeдлaгaется треxкомнaтная квapтирa oбщeй плoщадью 69 кв. м.,: куxня-гocтинaя (пeрепланиpoвка cогласовaна) и две oтдeльныe cпaльни, большой коpидoр с меcтaми для хpанения, гардepобная кoмнaта, тeплые пoлы в вaнной, кондиционeр в куxoннoй зоне, двe пpocтoрных лoджии, окнa нa две стороны. Квартира с мебелью, полностью готова к проживанию.", d, 20000000, 14,  1]
            cursor.execute(sql, parameters)
            d = datetime.now().date() - timedelta(days=24)
            parameters = [1, 3, common.get_adres(FALSE), 65, 8, 6, 13, "Прeдлaгaeм Вашeму вниманию простoрную тpехкомнатную квapтиру с гpaмoтнoй кoмфoртной планиpoвкой. Oкна выходят на двe стоpoны. Пpocторная гocтиная из котоpoй обoрудован прoxод на куxню, чтo позвoляет выдeлить cтоловую зону, oтдельнaя спaльня c выхoдном на зacтекленную лoджию, окнa из cпальни во двор и Комната свободного назначения с застеклённой лоджией ,возможно обустроить Кабинет или детскую комнату,", d, 23300000, 15,  0]            
            cursor.execute(sql, parameters)
        ##########################
        ##### view_zhile #####
        ##########################

        # Проверка наличия представления 
        cursor.execute("SELECT name FROM sqlite_master WHERE type='view' AND name='view_zhile'")
        result = cursor.fetchall()
        if len(result) > 0:
            print("Представление view_zhile уже существует")        
        else:
            print("Создается представление view_zhile")  
            create_table_query = '''CREATE VIEW view_zhile AS
                SELECT zhile.id, zhile.tip_id, tip.nazvanie AS tip, zhile.komnata, zhile.adres, zhile.polshchad1, zhile.polshchad2, zhile.etazh, zhile.etazhnost, 
                zhile.opisanie, zhile.data, zhile.price, zhile.klient_id, klient.fio AS prodavec, zhile.aktiv
                FROM zhile
                LEFT JOIN tip ON zhile.tip_id = tip.id
                LEFT JOIN klient ON zhile.klient_id = klient.id;'''
            # Выполнение команды: это создает новую таблицу
            cursor.execute(create_table_query)
            conn.commit()
            print("Представление view_zhile создано")      

        ###################
        ##### dogovor #####
        ###################

        # Проверка наличия таблицы 
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='dogovor'")
        result = cursor.fetchall()
        if len(result) > 0:
            print("Таблица dogovor уже существует")        
        else:
            print("Создается таблица dogovor")  
            create_table_query = '''CREATE TABLE dogovor (
                                id INTEGER NOT NULL,     
                                data_dogovora DATETIME NOT NULL,
								nomer_dogovora INTEGER NOT NULL,								
								zhile_id INTEGER NOT NULL,								
                                klient_id INTEGER NOT NULL,
							    price DECIMAL NOT NULL,
                                sotrudnik_id INTEGER NOT NULL,
                                PRIMARY KEY("id" AUTOINCREMENT),
                                FOREIGN KEY("zhile_id") REFERENCES "zhile"("id") ON DELETE CASCADE,
                                FOREIGN KEY("klient_id") REFERENCES "klient"("id") ON DELETE CASCADE,
                                FOREIGN KEY("sotrudnik_id") REFERENCES "sotrudnik"("id") ON DELETE CASCADE);'''
            # Выполнение команды: это создает новую таблицу
            cursor.execute(create_table_query)
            conn.commit()
            print("Таблица dogovor создана")        
        # Заполнение таблицы (один раз)
        sql = "SELECT id FROM dogovor"
        # С помощью метода execute объекта cursor можно выполнить запрос в базу данных из Python.
        # Он принимает SQL-запрос в качестве параметра и возвращает resultSet (строки базы данных):
        cursor.execute(sql)
        # Получить результат запроса из resultSet можно с помощью методов, например, fetchAll()
        row = cursor.fetchone()
        # Если таблица пустая - заполнить ее
        if row is None:
            sql = "INSERT INTO dogovor (data_dogovora, nomer_dogovora, zhile_id, klient_id, price, sotrudnik_id) VALUES (?, ?, ?, ?, ?, ?)"
            # Параметры запроса,  Выполнение запроса
            d = datetime.now().date() - timedelta(days=15)
            parameters = [d, 1, 1, 16, 1270000, 3]
            cursor.execute(sql, parameters)
            d = datetime.now().date() - timedelta(days=14)
            parameters = [d, 2, 5, 17, 22500000, 5]
            cursor.execute(sql, parameters)
            d = datetime.now().date() - timedelta(days=13)
            parameters = [d, 3, 9, 18, 17100000, 7]
            cursor.execute(sql, parameters)
            d = datetime.now().date() - timedelta(days=12)
            parameters = [d, 4, 13, 19, 28200000, 9]
            cursor.execute(sql, parameters)
            d = datetime.now().date() - timedelta(days=11)
            parameters = [d, 5, 15, 20, 23300000, 10]
            cursor.execute(sql, parameters)
            
        ##########################
        ##### view_dogovor #####
        ##########################

        # Проверка наличия представления 
        cursor.execute("SELECT name FROM sqlite_master WHERE type='view' AND name='view_dogovor'")
        result = cursor.fetchall()
        if len(result) > 0:
            print("Представление view_dogovor уже существует")        
        else:
            print("Создается представление view_dogovor")  
            create_table_query = '''CREATE VIEW view_dogovor AS
                SELECT dogovor.id, dogovor.data_dogovora, dogovor.nomer_dogovora, 
                dogovor.zhile_id, view_zhile.tip, view_zhile.komnata, view_zhile.adres, view_zhile.polshchad1, view_zhile.polshchad2, view_zhile.etazh, view_zhile.etazhnost, view_zhile.data, view_zhile.price AS zhile_price, view_zhile.prodavec, view_zhile.aktiv,
                dogovor.klient_id, klient.fio AS pokupatel,
                dogovor.price, 
                dogovor.sotrudnik_id, view_sotrudnik.fio AS sotrudnik
                FROM dogovor
                LEFT JOIN view_zhile ON dogovor.zhile_id = view_zhile.id
                LEFT JOIN klient ON dogovor.klient_id = klient.id
                LEFT JOIN view_sotrudnik ON dogovor.sotrudnik_id = view_sotrudnik.id;'''
            # Выполнение команды: это создает новую таблицу
            cursor.execute(create_table_query)
            conn.commit()
            print("Представление view_dogovor создано")     

        # Закрыть объект cursor после завершения работы.
        cursor.close()
        # Закрыть соединение после завершения работы.
        conn.close()
        print("База данных SQLite отключена")        
    except Exception as error:
        print(error)
 

###################
# Общие процедуры #
###################

# Выполнение параметрического запроса SQL (без возврата набора данных): sql - SQL-запрос, parameters - Параметры запроса
def executeSQL(sql, parameters):
    try:            
        # Подключение к БД 
        # Вызов функции connect() приводит к созданию объекта-экземпляра от класса Connection.
        # Этот объект обеспечивает связь с файлом базы данных, представляет конкретную БД в программе                             
        conn = connector.get_connection()
        # Объект cursor, позволяет взаимодействовать с базой данных             
        cursor = conn.cursor()            
        # Включить ограничения FOREIGN KEY 
        cursor.execute("PRAGMA foreign_keys=ON")                  
        # С помощью метода execute объекта cursor можно выполнить запрос в базу данных из Python.
        cursor.execute(sql, parameters)
        # Применить изменения в базе данных
        conn.commit()     
        # Закрыть объект cursor после завершения работы.
        cursor.close()
        # Закрыть соединение после завершения работы.
        conn.close()
        print(sql)
        return 1
    except Exception as error:
        print(error)
        return -1
    
# Возврат данных из таблицы БД (множество записей): sql - SQL-запрос на выборку данных
def fetchAll(sql):
    try:
        # Подключение к БД 
        # Вызов функции connect() приводит к созданию объекта-экземпляра от класса Connection.
        # Этот объект обеспечивает связь с файлом базы данных, представляет конкретную БД в программе                             
        conn = connector.get_connection()
        # Объект cursor, позволяет взаимодействовать с базой данных             
        cursor = conn.cursor()
        # С помощью метода execute объекта cursor можно выполнить запрос в базу данных из Python. Он принимает SQL-запрос в качестве параметра и возвращает resultSet (строки базы данных):
        cursor.execute(sql)
        # Получить результат запроса из resultSet можно с помощью методов, например, fetchall() или fetchone()
        rows = cursor.fetchall()            
        # Закрыть объект cursor после завершения работы.
        cursor.close()
        # Закрыть соединение после завершения работы.
        conn.close()
        # Вернуть результат проверки
        return rows
    except Exception as error:
        print(error)

# Возврат данных из таблицы БД (одна запись)
def fetchOne(sql):
    try:
        #print(sql)
        # Подключение к БД 
        # Вызов функции connect() приводит к созданию объекта-экземпляра от класса Connection.
        # Этот объект обеспечивает связь с файлом базы данных, представляет конкретную БД в программе                             
        conn = connector.get_connection()
        # Объект cursor, позволяет взаимодействовать с базой данных             
        cursor = conn.cursor()
        # С помощью метода execute объекта cursor можно выполнить запрос в базу данных из Python. Он принимает SQL-запрос в качестве параметра и возвращает resultSet (строки базы данных):
        cursor.execute(sql)
        # Получить результат запроса из resultSet можно с помощью методов, например, fetchall() или fetchone()
        result = cursor.fetchone()
        # Закрыть объект cursor после завершения работы.
        cursor.close()
        # Закрыть соединение после завершения работы.
        conn.close()
        # Вернуть результат проверки
        return result
    except Exception as error:
        print(error)
