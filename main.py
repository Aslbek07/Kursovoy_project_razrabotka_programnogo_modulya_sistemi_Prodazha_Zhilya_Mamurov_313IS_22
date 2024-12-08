# Импорт библиотек
from pickle import FALSE, TRUE
import sys
from turtle import title
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
# Подключаем модуль для SQLite
import sqlite3
# Подключаем модуль для работы с датой/временем
from datetime import datetime
# Подключаем модуль для работы с БД
import database
# Подключаем другие модули (инициализация, другие окна...)
import sotrudnik, dolzhnost, klient, tip, zhile, dogovor, polzovatel, report
# Подключаем сообщения
from messages import msg
# Модуль hashlib реализует общий интерфейс для множества различных безопасных алгоритмов хеширования и дайджеста сообщений
import hashlib
# Модуль os предоставляет множество функций для работы с операционной системой, причём их поведение, как правило, не зависит от ОС, поэтому программы остаются переносимыми. 
import os

# Создается новый класс ChangePasswordWindow котрый наследуется от класса QMainWindow. 
class ChangePasswordWindow(QMainWindow):
    def __init__(self, _id):
        try:
            super().__init__()
            # Считать id пользователя
            self.polzovatel_id = _id
            # Метод setGeometry() помещает окно на экране и устанавливает его размер.
            # Первые два параметра х и у - это позиция окна. Третий - ширина, и четвертый - высота окна.
            self.setGeometry(200, 200, 480, 240)
            # Заголовок окна
            self.setWindowTitle(msg.change_password)
            #self.setWindowIcon(QtGui.QIcon('logo.png'))
            self.setWindowIcon(QtGui.QIcon(':/images/logo.png'))
            ## Панели инструментов обеспечивают быстрый доступ к наиболее часто используемым командам.
            ## Создается действие с соответствующей иконкой.  
            #checkAction = QAction(QIcon(":/images/check.png"), msg.save, self)
            #stopAction = QAction(QIcon(":/images/stop.png"), msg.cancel, self)
            ##
            #checkAction.triggered.connect(lambda: self.update_data())
            #stopAction.triggered.connect(lambda: self.close())
            ## Метод addToolBar() создает панель инструментов.
            ## Создается кнопка и к ней добавляется действие.
            #self.toolbar = self.addToolBar("Toolbar")
            #self.toolbar.setIconSize(QSize(32,32))
            #self.toolbar.addAction(checkAction)
            #self.toolbar.addAction(stopAction)
            # Кнопки
            self.pushButtonUpdate = QPushButton(msg.save)
            self.pushButtonUpdate.clicked.connect(lambda: self.update_data())
            self.pushButtonCancel = QPushButton(msg.cancel)
            self.pushButtonCancel.clicked.connect(lambda: self.close())             
            # Метки
            self.label_login = QLabel(msg.login)
            self.label_password = QLabel(msg.password)
            self.label_new_password = QLabel(msg.new_password)
            self.label_confirm_password = QLabel(msg.confirm_password)
            # Поля ввода данных
            self.lineEdit_login = QLineEdit(self)
            self.lineEdit_login.setReadOnly(True)
            self.lineEdit_password = QLineEdit(self)
            self.lineEdit_password.setEchoMode(QLineEdit.Password)
            self.lineEdit_new_password = QLineEdit(self)
            self.lineEdit_new_password.setEchoMode(QLineEdit.Password)
            self.lineEdit_confirm_password = QLineEdit(self)
            self.lineEdit_confirm_password.setEchoMode(QLineEdit.Password)
            # Создаём центральный виджет
            central_widget = QWidget(self)
            # Устанавливаем центральный виджет
            self.setCentralWidget(central_widget)
            # Создаём QGridLayout -  сеточный макет который делит пространство на строки и столбцы. 
            grid_layout = QGridLayout()            
            # Устанавливаем данное размещение в центральный виджет
            central_widget.setLayout(grid_layout)
             # Добавляем все визуальные элементы в сетку
            # int fromRow — номер ряда, в который устанавливается верхняя левая часть виджета. Используется для случая, когда виджет необходимо разместить на несколько смежных ячеек.
            # int fromColumn — номер столбца, в который устанавливается верхняя левая часть виджета. Используется для случая, когда виджет необходимо разместить на несколько смежных ячеек.
            # int rowSpan — количество рядов, ячейки которых следует объединить для размещения виджета начиная с ряда fromRow.
            # int columnSpan — количество столбцов, ячейки которых следует объединить для размещения виджета начиная со столбца fromColumn.
            grid_layout.addWidget(self.label_login, 0, 0, 1, 1)
            grid_layout.addWidget(self.lineEdit_login, 0, 1, 1, 3) 
            grid_layout.addWidget(self.label_password, 1, 0, 1, 1) 
            grid_layout.addWidget(self.lineEdit_password, 1, 1, 1, 3)    
            grid_layout.addWidget(self.label_new_password, 2, 0, 1, 1) 
            grid_layout.addWidget(self.lineEdit_new_password, 2, 1, 1, 3)             
            grid_layout.addWidget(self.label_confirm_password, 3, 0, 1, 1) 
            grid_layout.addWidget(self.lineEdit_confirm_password, 3, 1, 1, 3)        
            grid_layout.addWidget(self.pushButtonUpdate, 4, 0, 1, 2) 
            grid_layout.addWidget(self.pushButtonCancel, 4, 2, 1, 2)
            # Считать пользователя
            self.read_record()                     
            # Выравнивание окна по центру
            # Класс QtWidgets.QDesktopWidget предоставляет информацию о компьютере пользователя, в том числе о размерах экрана. Получаем прямоугольник, определяющий геометрию главного окна. Это включает в себя любые рамки окна.
            qr = self.frameGeometry()
            # Получаем разрешение экрана монитора, и с этим разрешением, мы центральную точку
            cp = QDesktopWidget().availableGeometry().center()
            # Наш прямоугольник уже имеет ширину и высоту. Теперь мы установили центр прямоугольника в центре экрана. Размер прямоугольника не изменяется.
            qr.moveCenter(cp)
            # Двигаем верхний левый угол окна приложения в верхний левый угол прямоугольника qr, таким образом, центрируя окно на нашем экране.
            self.move(qr.topLeft())
        except Exception as error:
            print(error)
            QMessageBox.critical(self,  "Error",  str(error))   

    def read_record(self):
        try:
            # SQL-запрос новая чтения записи
            sql = "SELECT login FROM polzovatel WHERE id=" + str(self.polzovatel_id)
            # Получить результат запроса из resultSet можно с помощью методов, например, fetchall() или fetchone()   
            results = database.fetchOne(sql)
            self.lineEdit_login.setText(results[0])            
        except Exception as error:
            print(error)
            QMessageBox.critical(self,  "Error",  str(error))   

    def update_data(self):
        try:
            # Проверка данных
            if self.lineEdit_password.text() == "" or self.lineEdit_new_password.text() == "" or self.lineEdit_confirm_password.text() == "":
                # Окно с информационным сообщением. Первая строка отображается в заголовке окна, вторая - в сообщении.
                QMessageBox.warning(self, msg.warning, msg.fill_all_fields)
                return   
            # SQL-запрос
            sql = "SELECT parol FROM polzovatel WHERE id=" + str(self.polzovatel_id)
            # Получить результат запроса из resultSet можно с помощью методов, например, fetchall() или fetchone()   
            results = database.fetchOne(sql)
            parol = results[0]
            # Собственно проверка
            #if self.lineEdit_password.text() != parol:
            if hashlib.sha256(self.lineEdit_password.text().encode('utf-8')).hexdigest() != parol:
                # Окно с информационным сообщением. Первая строка отображается в заголовке окна, вторая - в сообщении.
                QMessageBox.warning(self, msg.warning, msg.invalid_old_password)
                return     
            if len(self.lineEdit_new_password.text()) < 4:
                # Окно с информационным сообщением. Первая строка отображается в заголовке окна, вторая - в сообщении.
                QMessageBox.warning(self, msg.warning, msg.minimum_password_length_4_characters)
                return 
            if self.lineEdit_new_password.text() != self.lineEdit_confirm_password.text() :
                # Окно с информационным сообщением. Первая строка отображается в заголовке окна, вторая - в сообщении.
                QMessageBox.warning(self, msg.warning, msg.password_and_confirmation_do_not_match)
                return 
            # Изменение данных
            # SQL-запрос новая запись или изменение записи            
            #sql = "UPDATE polzovatel SET parol='" + self.lineEdit_new_password.text() + "' WHERE id=" + str(self.polzovatel_id)
            sql = "UPDATE polzovatel SET parol=? WHERE id=?"
            # Параметры запроса
            parameters = [hashlib.sha256(self.lineEdit_new_password.text().encode('utf-8')).hexdigest(), self.polzovatel_id]
            # Выполнить запрос sql c параметрами parameters
            database.executeSQL(sql, parameters)
            # Окно с информационным сообщением. Первая строка отображается в заголовке окна, вторая - в сообщении.
            QMessageBox.information(self, "", msg.password_changed_successfully)
            # Закрыть окно
            self.close()
        except Exception as error:
            print(error)
            QMessageBox.critical(self,  "Error",  str(error))   
    #def closeEvent(self, event):        
    #    # Обновить данные в таблице при закрытии окна
    #    self.select_data("")

# Создается новый класс LoginWindow котрый наследуется от класса QMainWindow. 
class LoginWindow(QMainWindow):
    def __init__(self):
        try:
            super().__init__()
            flag=FALSE
            # Метод setGeometry() помещает окно на экране и устанавливает его размер.
            # Первые два параметра х и у - это позиция окна. Третий - ширина, и четвертый - высота окна.
            self.setGeometry(200, 200, 350, 150)
            # Заголовок окна
            self.setWindowTitle(msg.authorization)
            #self.setWindowIcon(QtGui.QIcon('logo.png'))
            self.setWindowIcon(QtGui.QIcon(':/images/logo.png'))
            ## Панели инструментов обеспечивают быстрый доступ к наиболее часто используемым командам.
            ## Создается действие с соответствующей иконкой.  
            #loginAction = QAction(QIcon(":/images/check.png"), msg.login, self)            
            #exitAction = QAction(QIcon(":/images/exit.png"), msg.exit, self)
            ## Для этого действия определяется комбинация клавиш.
            #exitAction.setShortcut("Ctrl+Q")
            ##
            #loginAction.triggered.connect(lambda: self.check_login())
            #exitAction.triggered.connect(lambda: self.close())
            ## Метод addToolBar() создает панель инструментов.
            ## Создается кнопка и к ней добавля.тся действие.
            #self.toolbar = self.addToolBar("Toolbar")
            #self.toolbar.setIconSize(QSize(32,32))
            #self.toolbar.addAction(loginAction)
            #self.toolbar.addAction(exitAction)

            # Метки
            label_login = QLabel(msg.login)
            label_password = QLabel(msg.password)
            # Поля ввода данных
            self.lineEdit_login = QLineEdit(self)
            self.lineEdit_password = QLineEdit(self)
            self.lineEdit_password.setEchoMode(QLineEdit.Password)
            # Кнопки
            self.pushButtonOk = QPushButton(msg.ok)
            self.pushButtonOk.clicked.connect(lambda: self.check_login())
            self.pushButtonCancel = QPushButton(msg.cancel)
            self.pushButtonCancel.clicked.connect(lambda: self.close())  
            # Создаём центральный виджет
            central_widget = QWidget(self)
            # Устанавливаем центральный виджет
            self.setCentralWidget(central_widget)
            # Создаём QGridLayout -  сеточный макет который делит пространство на строки и столбцы. 
            grid_layout = QGridLayout()            
            # Устанавливаем данное размещение в центральный виджет
            central_widget.setLayout(grid_layout)
             # Добавляем все визуальные элементы в сетку
            # int fromRow — номер ряда, в который устанавливается верхняя левая часть виджета. Используется для случая, когда виджет необходимо разместить на несколько смежных ячеек.
            # int fromColumn — номер столбца, в который устанавливается верхняя левая часть виджета. Используется для случая, когда виджет необходимо разместить на несколько смежных ячеек.
            # int rowSpan — количество рядов, ячейки которых следует объединить для размещения виджета начиная с ряда fromRow.
            # int columnSpan — количество столбцов, ячейки которых следует объединить для размещения виджета начиная со столбца fromColumn.
            grid_layout.addWidget(label_login, 0, 0, 1, 1)
            grid_layout.addWidget(self.lineEdit_login, 0, 1, 1, 3)            
            grid_layout.addWidget(label_password, 1, 0, 1, 1)
            grid_layout.addWidget(self.lineEdit_password, 1, 1, 1, 3)
            grid_layout.addWidget(self.pushButtonOk, 2, 0, 1, 2)
            grid_layout.addWidget(self.pushButtonCancel, 2, 2, 1, 2)
            # Выравнивание окна по центру
            # Класс QtWidgets.QDesktopWidget предоставляет информацию о компьютере пользователя, в том числе о размерах экрана. Получаем прямоугольник, определяющий геометрию главного окна. Это включает в себя любые рамки окна.
            qr = self.frameGeometry()
            # Получаем разрешение экрана монитора, и с этим разрешением, мы центральную точку
            cp = QDesktopWidget().availableGeometry().center()
            # Наш прямоугольник уже имеет ширину и высоту. Теперь мы установили центр прямоугольника в центре экрана. Размер прямоугольника не изменяется.
            qr.moveCenter(cp)
            # Двигаем верхний левый угол окна приложения в верхний левый угол прямоугольника qr, таким образом, центрируя окно на нашем экране.
            self.move(qr.topLeft())
            # На время отладки
            #self.lineEdit_login.setText("manager");
            #self.lineEdit_password.setText("manager");
        except Exception as error:
            print(error)
            QMessageBox.critical(self, "Error",  str(error))   

    def check_login(self):
        try:
            # Проверка данных
            if self.lineEdit_login.text() == "" or self.lineEdit_password.text() == "" :
                # Окно с информационным сообщением. Первая строка отображается в заголовке окна, вторая - в сообщении.
                QMessageBox.warning(self,  msg.warning,  msg.fill_all_fields)
                return     
            # SQL-запрос новая чтения записи
            #sql = "SELECT id, login, parol, administrator, menedzher FROM polzovatel WHERE login='" + self.lineEdit_login.text() + "' AND parol='" + self.lineEdit_password.text() + "'"
            sql = "SELECT id, login, parol, administrator, menedzher FROM polzovatel WHERE login='" + self.lineEdit_login.text() + "' AND parol='" + hashlib.sha256(self.lineEdit_password.text().encode('utf-8')).hexdigest() + "'"
            # Получить результат запроса из resultSet можно с помощью методов, например, fetchall() или fetchone()
            result = database.fetchOne(sql)
            id = 0;
            adm = False;
            man = False;
            # Вызов окна с передачей ролей
            if result != None:
                id = result[0]
                adm = result[3]
                man = result[4]
                #print(id)
                #print(adm)
                #print(man)
                # Скрыть окно с логином и паролем
                self.setVisible(False)
                main_window = MainWindow(id, adm, man)
                main_window.show() 
            else:
                QMessageBox.warning(self,  msg.warning,  msg.Incorrect_login_or_password)                
        except Exception as error:
            print(error)
            QMessageBox.critical(self,  "Error",  str(error))   

# Создается новый класс MainWindow котрый наследуется от класса QMainWindow. 
class MainWindow(QMainWindow):
    # Роль пользователя
    polzovatel_id = 0
    admin = False
    manager = False
    # Условие (WHERE) и порядок сортировки (ORDER)
    where = ""
    order = ""
    # Класс MainWindow наследуется от класса QWidget. Это означает, что мы вызываем два конструктора:
    # первый для класса MainWindow и второй для родительского класса.
    # Функция super() возвращает родительский объект MainWindow с классом, и мы вызываем его конструктор.    
    def __init__(self, i, a, m):
        super().__init__()       
        self.polzovatel_id = i
        self.admin = a
        self.manager = m
        # Создание GUI делегируется методу initUI().
        self.initUI()
    def initUI(self):
        try:
            # Метод setGeometry() помещает окно на экране и устанавливает его размер.
            # Первые два параметра х и у - это позиция окна. Третий - ширина, и четвертый - высота окна.
            self.setGeometry(200, 200, 800, 600)
            #print(self.polzovatel_id)
            #print(self.admin)
            #print(self.manager )
            # Заголовок окна
            self.setWindowTitle(msg.app_name)
            #self.setWindowIcon(QtGui.QIcon('logo.png'))
            self.setWindowIcon(QtGui.QIcon(':/images/logo.png'))
            ## Панели инструментов обеспечивают быстрый доступ к наиболее часто используемым командам.
            ## Создается действие с соответствующей иконкой.  
            #sotrudnikAction = QAction(QIcon(":/images/contact.png"), msg.sotrudnik, self)
            #dolzhnostAction = QAction(QIcon(":/images/descending.png"), msg.dolzhnost, self)
            #polzovatelAction = QAction(QIcon(":/images/group.png"), msg.polzovatel, self)
            #exitAction = QAction(QIcon(":/images/exit.png"), msg.exit, self)
            ## Для этого действия определяется комбинация клавиш.
            #exitAction.setShortcut("Ctrl+Q")
            ##
            #sotrudnikAction.triggered.connect(lambda: self.change_sotrudnik())
            #dolzhnostAction.triggered.connect(lambda: self.change_dolzhnost())
            #polzovatelAction.triggered.connect(lambda: self.change_polzovatel())
            #exitAction.triggered.connect(lambda: self.close())
            ## Метод addToolBar() создает панель инструментов.
            ## Создается кнопка и к ней добавляется действие.
            #self.toolbar = self.addToolBar("Toolbar")
            #self.toolbar.setIconSize(QSize(32,32))
            ##self.toolbar.setIconSize(QSize(48,48))
            #if self.admin != False:                
            #    self.toolbar.addAction(sotrudnikAction)
            #    self.toolbar.addAction(dolzhnostAction)
            #else:
            #    self.toolbar.addAction(polzovatelAction)
            #self.toolbar.addAction(exitAction)
            
            # Главное меню
            self.menuBar = self.menuBar()
            # Меню Файл
            self.exitAction = QAction(msg.exit, self)
            self.exitAction.triggered.connect(lambda: self.close())
            self.sotrudnikAction = QAction(msg.sotrudniki, self)
            self.sotrudnikAction.triggered.connect(lambda: self.change_sotrudnik())
            self.klientAction = QAction(msg.klienty, self)
            self.klientAction.triggered.connect(lambda: self.change_klient())
            self.zhileAction = QAction(msg.zhile, self)
            self.zhileAction.triggered.connect(lambda: self.change_zhile())
            self.dogovorAction = QAction(msg.dogovora, self)
            self.dogovorAction.triggered.connect(lambda: self.change_dogovor())
            self.polzovatelAction = QAction(msg.polzovateli, self)
            self.polzovatelAction.triggered.connect(lambda: self.change_polzovatel())
            self.reportAction = QAction(msg.reports, self)
            self.reportAction.triggered.connect(lambda: self.report())            
            self.passwordAction = QAction(msg.change_password, self)
            self.passwordAction.triggered.connect(lambda: self.change_password())            
            self.fileMenu = self.menuBar.addMenu(msg.file)
            if self.manager == True: 
                self.fileMenu.addAction(self.sotrudnikAction)
                self.fileMenu.addAction(self.klientAction)
                self.fileMenu.addAction(self.zhileAction)
                self.fileMenu.addAction(self.dogovorAction)
                self.fileMenu.addSeparator()                            
            if self.admin == True:
                self.fileMenu.addAction(self.polzovatelAction)
            self.fileMenu.addSeparator()
            self.fileMenu.addAction(self.reportAction)
            self.fileMenu.addSeparator()            
            self.fileMenu.addAction(self.passwordAction)            
            self.fileMenu.addSeparator()
            self.fileMenu.addAction(self.exitAction)
            # Справочники
            if self.manager == True: 
                self.dolzhnostAction = QAction(msg.dolzhnosti, self) 
                self.dolzhnostAction.triggered.connect(lambda: self.change_dolzhnost())
                self.tipAction = QAction(msg.tipy, self) 
                self.tipAction.triggered.connect(lambda: self.change_tip())
                self.sprMenu = self.menuBar.addMenu(msg.spr)
                self.sprMenu.addAction(self.dolzhnostAction)            
                self.sprMenu.addAction(self.tipAction)            
            # Создаём таблицу
            self.tableWidget = QTableWidget(self)  
            # Разные цвета для четных и нечетных строк
            self.tableWidget.setAlternatingRowColors(True);
            # Запрет изменения таблицы
            self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            # Устанавливаем количество колонок
            self.tableWidget.setColumnCount(12)
            # Устанавливаем заголовки таблицы
            self.tableWidget.setHorizontalHeaderLabels([msg.id, msg.tip, msg.komnata, msg.adres, msg.polshchad1, msg.polshchad2, 
                                                        msg.etazh, msg.etazhnost, msg.data, msg.price, msg.prodavec, msg.aktiv])
            # GroupBox сортировки
            self.groupBox_sort = QGroupBox(msg.sorting)
            #self.groupBox_sort.setMaximumHeight(300)
            self.groupBoxLayout_sort = QVBoxLayout()
            self.groupBox_sort.setLayout(self.groupBoxLayout_sort)            
            # Список сортировки 
            self.comboBox_sort = QComboBox(self)
            self.comboBox_sort.addItem(msg.id, 0) 
            self.comboBox_sort.addItem(msg.tip, 1) 
            self.comboBox_sort.addItem(msg.komnata, 2) 
            self.comboBox_sort.addItem(msg.adres, 3) 
            self.comboBox_sort.addItem(msg.polshchad1, 4) 
            self.comboBox_sort.addItem(msg.polshchad2, 5) 
            self.comboBox_sort.addItem(msg.etazh, 6) 
            self.comboBox_sort.addItem(msg.etazhnost, 7) 
            self.comboBox_sort.addItem(msg.data, 8) 
            self.comboBox_sort.addItem(msg.price, 9) 
            self.comboBox_sort.addItem(msg.prodavec, 10) 
            self.comboBox_sort.addItem(msg.aktiv, 11) 
            self.comboBox_sort.currentTextChanged.connect(lambda: self.change_comboBox_sort())
            # Checkbox-ы
            self.checkBox_desc = QCheckBox(msg.reverse_sort, self)
            self.checkBox_desc.stateChanged.connect(lambda: self.change_comboBox_sort())
            # Добавляем визуальные элементы 
            self.groupBoxLayout_sort.addWidget(self.comboBox_sort)
            self.groupBoxLayout_sort.addWidget(self.checkBox_desc)
            # GroupBox фильтра
            self.groupBox_filter = QGroupBox(msg.filter)
            #self.groupBox_filter.setMaximumHeight(200)
            self.grid_layout_filter = QGridLayout()
            self.groupBox_filter.setLayout(self.grid_layout_filter)
            # Метки
            self.label_tip = QLabel(msg.tip)
            self.label_komnata = QLabel(msg.komnata)
            self.label_adres = QLabel(msg.adres) 
            self.label_polshchad1 = QLabel(msg.polshchad1)
            self.label_polshchad2 = QLabel(msg.polshchad2)
            self.label_etazh = QLabel(msg.etazh)
            self.label_etazhnost = QLabel(msg.etazhnost)
            self.label_data = QLabel(msg.data)
            self.label_price = QLabel(msg.price)
            self.label_prodavec = QLabel(msg.prodavec)
            #self.label_aktiv = QLabel(msg.aktiv)
            # Поля ввода данных
            self.lineEdit_tip = QLineEdit(self)
            self.lineEdit_komnata_1 = QLineEdit(self)
            self.lineEdit_komnata_2 = QLineEdit(self)
            self.lineEdit_adres = QLineEdit(self)
            self.lineEdit_polshchad1_1 = QLineEdit(self)
            self.lineEdit_polshchad1_2 = QLineEdit(self)
            self.lineEdit_polshchad2_1 = QLineEdit(self) 
            self.lineEdit_polshchad2_2 = QLineEdit(self) 
            self.lineEdit_etazh_1 = QLineEdit(self) 
            self.lineEdit_etazh_2 = QLineEdit(self) 
            self.lineEdit_etazhnost_1 = QLineEdit(self) 
            self.lineEdit_etazhnost_2 = QLineEdit(self) 
            self.lineEdit_data_1 = QLineEdit(self) 
            self.lineEdit_data_2 = QLineEdit(self) 
            self.lineEdit_price_1 = QLineEdit(self) 
            self.lineEdit_price_2 = QLineEdit(self) 
            self.lineEdit_prodavec = QLineEdit(self) 
            #self.lineEdit_aktiv = QLineEdit(self) 
            # Кнопки
            self.pushButtonFilter = QPushButton(msg.filter)
            self.pushButtonFilter.clicked.connect(lambda: self.set_filter())
            self.pushButtonCancel = QPushButton(msg.cancel)
            self.pushButtonCancel.clicked.connect(lambda: self.reset_filter())
            # Добавляем визуальные элементы в сетку
            self.grid_layout_filter.addWidget(self.label_tip, 0, 0, 1, 1)
            self.grid_layout_filter.addWidget(self.lineEdit_tip, 0, 1, 1, 1)
            self.grid_layout_filter.addWidget(self.label_komnata, 1, 0, 1, 1)
            self.grid_layout_filter.addWidget(self.lineEdit_komnata_1, 1, 1, 1, 1)
            self.grid_layout_filter.addWidget(self.lineEdit_komnata_2, 1, 2, 1, 1)
            self.grid_layout_filter.addWidget(self.label_adres, 2, 0, 1, 1)
            self.grid_layout_filter.addWidget(self.lineEdit_adres, 2, 1, 1, 1)
            self.grid_layout_filter.addWidget(self.label_polshchad1, 3, 0, 1, 1)
            self.grid_layout_filter.addWidget(self.lineEdit_polshchad1_1, 3, 1, 1, 1)
            self.grid_layout_filter.addWidget(self.lineEdit_polshchad1_2, 3, 2, 1, 1)
            self.grid_layout_filter.addWidget(self.label_polshchad2, 4, 0, 1, 1)
            self.grid_layout_filter.addWidget(self.lineEdit_polshchad2_1, 4, 1, 1, 1)            
            self.grid_layout_filter.addWidget(self.lineEdit_polshchad2_2, 4, 2, 1, 1)            
            self.grid_layout_filter.addWidget(self.label_etazh, 0, 3, 1, 1)
            self.grid_layout_filter.addWidget(self.lineEdit_etazh_1, 0, 4, 1, 1)
            self.grid_layout_filter.addWidget(self.lineEdit_etazh_2, 0, 5, 1, 1)
            self.grid_layout_filter.addWidget(self.label_etazhnost, 1, 3, 1, 1)
            self.grid_layout_filter.addWidget(self.lineEdit_etazhnost_1, 1, 4, 1, 1)
            self.grid_layout_filter.addWidget(self.lineEdit_etazhnost_2, 1, 5, 1, 1)
            self.grid_layout_filter.addWidget(self.label_data, 2, 3, 1, 1)
            self.grid_layout_filter.addWidget(self.lineEdit_data_1, 2, 4, 1, 1)
            self.grid_layout_filter.addWidget(self.lineEdit_data_2, 2, 5, 1, 1)
            self.grid_layout_filter.addWidget(self.label_price, 3, 3, 1, 1)
            self.grid_layout_filter.addWidget(self.lineEdit_price_1, 3, 4, 1, 1)
            self.grid_layout_filter.addWidget(self.lineEdit_price_2, 3, 5, 1, 1)
            self.grid_layout_filter.addWidget(self.label_prodavec, 4, 3, 1, 1)
            self.grid_layout_filter.addWidget(self.lineEdit_prodavec, 4, 4, 1, 1)
            self.grid_layout_filter.addWidget(self.pushButtonFilter, 5, 4, 1, 1)
            self.grid_layout_filter.addWidget(self.pushButtonCancel, 5, 5, 1, 1)
            # Создаём центральный виджет
            central_widget = QWidget(self)
            # Устанавливаем центральный виджет
            self.setCentralWidget(central_widget)
            # Создаём QGridLayout -  сеточный макет который делит пространство на строки и столбцы. 
            grid_layout = QGridLayout()            
            # Устанавливаем данное размещение в центральный виджет
            central_widget.setLayout(grid_layout)               
            ## Добавляем все визуальные элементы в сетку
            ## int fromRow — номер ряда, в который устанавливается верхняя левая часть виджета. Используется для случая, когда виджет необходимо разместить на несколько смежных ячеек.
            ## int fromColumn — номер столбца, в который устанавливается верхняя левая часть виджета. Используется для случая, когда виджет необходимо разместить на несколько смежных ячеек.
            ## int rowSpan — количество рядов, ячейки которых следует объединить для размещения виджета начиная с ряда fromRow.
            ## int columnSpan — количество столбцов, ячейки которых следует объединить для размещения виджета начиная со столбца fromColumn.
            ## Ячейка начинается с первой строки и нулевой колонки, и занимает 1 строку и 4 колонки.
            grid_layout.addWidget(self.groupBox_sort, 0, 0, 1, 5)
            grid_layout.addWidget(self.groupBox_filter, 1, 0, 1, 5)
            grid_layout.addWidget(self.tableWidget, 2, 0, 1, 5)     
            # Выравнивание окна по центру
            # Класс QtWidgets.QDesktopWidget предоставляет информацию о компьютере пользователя, в том числе о размерах экрана. Получаем прямоугольник, определяющий геометрию главного окна. Это включает в себя любые рамки окна.
            qr = self.frameGeometry()
            # Получаем разрешение экрана монитора, и с этим разрешением, мы центральную точку
            cp = QDesktopWidget().availableGeometry().center()
            # Наш прямоугольник уже имеет ширину и высоту. Теперь мы установили центр прямоугольника в центре экрана. Размер прямоугольника не изменяется.
            qr.moveCenter(cp)
            # Двигаем верхний левый угол окна приложения в верхний левый угол прямоугольника qr, таким образом, центрируя окно на нашем экране.
            self.move(qr.topLeft())
            # Список
            self.select_data() 
        except Exception as error:
            print(error)
            QMessageBox.critical(self,  "Error",  str(error))   

    def change_comboBox_sort(self):
        try:
            # Изменение списка сортировки
            #print(self.comboBox_sort.currentText())
            #print(self.comboBox_sort.currentIndex())
            if self.comboBox_sort.currentIndex() == 0:
                sorting = "ORDER BY id"
            elif self.comboBox_sort.currentIndex() == 1:
                sorting = "ORDER BY tip" 
            elif self.comboBox_sort.currentIndex() == 2:
                sorting = "ORDER BY komnata" 
            elif self.comboBox_sort.currentIndex() == 3:
                sorting = "ORDER BY adres" 
            elif self.comboBox_sort.currentIndex() == 4:
                sorting = "ORDER BY polshchad1" 
            elif self.comboBox_sort.currentIndex() == 5:
                sorting = "ORDER BY polshchad2" 
            elif self.comboBox_sort.currentIndex() == 6:
                sorting = "ORDER BY etazh" 
            elif self.comboBox_sort.currentIndex() == 7:
                sorting = "ORDER BY etazhnost" 
            elif self.comboBox_sort.currentIndex() == 8:
                sorting = "ORDER BY data" 
            elif self.comboBox_sort.currentIndex() == 9:
                sorting = "ORDER BY price" 
            elif self.comboBox_sort.currentIndex() == 10:
                sorting = "ORDER BY prodavec" 
            elif self.comboBox_sort.currentIndex() == 11:
                sorting = "ORDER BY aktiv" 
            else:
                sorting = "ORDER BY " + self.comboBox_sort.currentText()
            if self.checkBox_desc.isChecked():
                sorting = sorting + " DESC "  
            self.order = sorting
            #print(self.where)
            #print(self.order)
            # Обновить список
            self.select_data() 
        except Exception as error:
            print(error)
            QMessageBox.critical(self,  "Error",  str(error))    
   
    def set_filter(self):
        try:
            # Изменение фильтра
            condition = ""
            if self.lineEdit_tip.text() != "":
                condition = condition + "tip LIKE '%" + self.lineEdit_tip.text() + "%' AND "
            if self.lineEdit_komnata_1.text() != "":
                if self.lineEdit_komnata_2.text() != "":
                    condition = condition + "komnata >= " + self.lineEdit_komnata_1.text() + " AND " + "komnata <= " + self.lineEdit_komnata_2.text() + " AND "
                else:
                    condition = condition + "komnata = " + self.lineEdit_komnata_1.text() + " AND "
            if self.lineEdit_adres.text() != "":
                condition = condition + "adres LIKE '%" + self.lineEdit_adres.text() + "%' AND "
            if self.lineEdit_polshchad1_1.text() != "":
                if self.lineEdit_polshchad1_2.text() != "":
                    condition = condition + "polshchad1 >= " + self.lineEdit_polshchad1_1.text() + " AND " + "polshchad1 <= " + self.lineEdit_polshchad1_2.text() + " AND "
                else:
                    condition = condition + "polshchad1 = " + self.lineEdit_polshchad1_1.text() + " AND "
            if self.lineEdit_polshchad2_1.text() != "":
                if self.lineEdit_polshchad2_2.text() != "":
                    condition = condition + "polshchad2 >= " + self.lineEdit_polshchad2_1.text() + " AND " + "polshchad2 <= " + self.lineEdit_polshchad2_2.text() + " AND "
                else:
                    condition = condition + "polshchad2 = " + self.lineEdit_polshchad2_1.text() + " AND "
            if self.lineEdit_etazh_1.text() != "":
                if self.lineEdit_etazh_2.text() != "":
                    condition = condition + "etazh >= " + self.lineEdit_etazh_1.text() + " AND " + "etazh <= " + self.lineEdit_etazh_2.text() + " AND "
                else:
                    condition = condition + "etazh = " + self.lineEdit_etazh_1.text() + " AND "
            if self.lineEdit_etazhnost_1.text() != "":
                if self.lineEdit_etazhnost_2.text() != "":
                    condition = condition + "etazhnost >= " + self.lineEdit_etazhnost_1.text() + " AND " + "etazhnost <= " + self.lineEdit_etazhnost_2.text() + " AND "
                else:
                    condition = condition + "etazhnost = " + self.lineEdit_etazhnost_1.text() + " AND "
            if self.lineEdit_data_1.text() != "":
                if self.lineEdit_data_2.text() != "":
                    qdateData1 = QtCore.QDate.fromString(str(self.lineEdit_data_1.text()[0:10]), "dd.MM.yyyy")
                    qdateData2 = QtCore.QDate.fromString(str(self.lineEdit_data_2.text()[0:10]), "dd.MM.yyyy")
                    condition = condition + "data >= '" + str(qdateData1.toPyDate()) + "' AND " + "data <= '" + str(qdateData2.toPyDate()) + "' AND "
                else:
                    qdateData = QtCore.QDate.fromString(str(self.lineEdit_data_1.text()[0:10]), "dd.MM.yyyy")
                    condition = condition + "data = '" +  str(qdateData.toPyDate()) + "' AND "
            if self.lineEdit_price_1.text() != "":
                if self.lineEdit_price_2.text() != "":
                    condition = condition + "price >= " + self.lineEdit_price_1.text() + " AND " + condition + "price <= " + self.lineEdit_price_2.text() + " AND "
                else:
                    condition = condition + "price = " + self.lineEdit_price_1.text() + " AND "
            if self.lineEdit_prodavec.text() != "":
                condition = condition + "prodavec LIKE '%" + self.lineEdit_prodavec.text() + "%' AND "
            # Добавление WHERE Отсечение AND
            if condition != "":
                condition = "AND " + condition[:-4]
            self.where = condition
            print(self.where)
            #print(self.order)
            # Обновить список
            self.select_data() 
        except Exception as error:
            print(error)
            QMessageBox.critical(self,  "Error",  str(error))          

    def reset_filter(self):
        try:
            # Сброс фильтра
            self.lineEdit_tip.setText("")
            self.lineEdit_komnata_1.setText("")
            self.lineEdit_komnata_2.setText("")
            self.lineEdit_adres.setText("")
            self.lineEdit_polshchad1_1.setText("")
            self.lineEdit_polshchad1_2.setText("")
            self.lineEdit_polshchad2_1.setText("")
            self.lineEdit_polshchad2_2.setText("")
            self.lineEdit_etazh_1.setText("")
            self.lineEdit_etazh_2.setText("")
            self.lineEdit_etazhnost_1.setText("")
            self.lineEdit_etazhnost_2.setText("")
            self.lineEdit_data_1.setText("")
            self.lineEdit_data_2.setText("")
            self.lineEdit_price_1.setText("")
            self.lineEdit_price_2.setText("")
            self.lineEdit_prodavec.setText("")
            # Обновить список
            self.where = ""
            self.order = ""
            self.select_data() 
        except Exception as error:
            print(error)
            QMessageBox.critical(self,  "Error",  str(error))      

    def select_data(self):
        try:
            # SQL-запрос
            sql = "SELECT id, tip, komnata, adres, polshchad1, polshchad2, etazh, etazhnost, strftime('%d.%m.%Y', data) AS data_, price, prodavec, aktiv FROM view_zhile WHERE aktiv = 1 " + self.where + " " + self.order
            # Получить результат запроса из resultSet можно с помощью методов, например, fetchall() или fetchone()
            result = database.fetchAll(sql)
            # Установить количество строк
            self.tableWidget.setRowCount(0)
            self.tableWidget.setRowCount(len(result))
            # Установить количество строк
            self.tableWidget.setRowCount(0)
            self.tableWidget.setRowCount(len(result))
            # Заполнить таблицу
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    if val != None:
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))  
            # Ресайз колонок по содержимому
            self.tableWidget.resizeColumnsToContents()
            ## Сброс строки поиска
            #if where=="":
            #    self.lineEdit.setText("")
        except Exception as error:
            print(error)
            QMessageBox.critical(self,  msg.error,  str(error))   

    def change_sotrudnik(self):
        try:
            # Вызов дочернего окна (Сотрудники)
            self.sotrudnik_window = sotrudnik.SotrudnikListWindow()  
            self.sotrudnik_window.show()            
        except Exception as error:
            print(error)
            QMessageBox.critical(self,  "Error",  str(error))   
            
    def change_dolzhnost(self):
        try:
            # Вызов дочернего окна (справочник)
            self.dolzhnost_window = dolzhnost.DolzhnostListWindow()  
            self.dolzhnost_window.show()            
        except Exception as error:
            print(error)
            QMessageBox.critical(self,  "Error",  str(error))   
            
    def change_klient(self):
        try:
            # Вызов дочернего окна (Клиенты)
            self.klient_window = klient.KlientListWindow()  
            self.klient_window.show()            
        except Exception as error:
            print(error)
            QMessageBox.critical(self,  "Error",  str(error))   

    def change_tip(self):
        try:
            # Вызов дочернего окна (справочник)
            self.tip_window = tip.TipListWindow()  
            self.tip_window.show()            
        except Exception as error:
            print(error)
            QMessageBox.critical(self,  "Error",  str(error))   

    def change_zhile(self):
        try:
            # Вызов дочернего окна (Жилье)
            self.zhile_window = zhile.ZhileListWindow()  
            self.zhile_window.show()            
        except Exception as error:
            print(error)
            QMessageBox.critical(self,  "Error",  str(error))   

    def change_dogovor(self):
        try:
            # Вызов дочернего окна (Договора)
            self.dogovor_window = dogovor.DogovorListWindow()  
            self.dogovor_window.show()            
        except Exception as error:
            print(error)
            QMessageBox.critical(self,  "Error",  str(error))   
            
    def change_polzovatel(self):
        try:
            # Вызов дочернего окна (пользователи)
            self.polzovatel_window = polzovatel.PolzovatelListWindow()  
            self.polzovatel_window.show()            
        except Exception as error:
            print(error)
            QMessageBox.critical(self,  "Error",  str(error))   
    
    def report(self):
        try:
            # Вызов дочернего окна (Отчеты...)
            self.report_window = report.ReportWindow()  
            self.report_window.show()            
        except Exception as error:
            print(error)
            QMessageBox.critical(self,  "Error",  str(error))   
            
    def change_password(self):
        try:
            # Вызов дочернего окна (Сменить пароль)
            self.change_password_window = ChangePasswordWindow(self.polzovatel_id)            
            self.change_password_window.show()
        except Exception as error:
            print(error)
            QMessageBox.critical(self,  "Error",  str(error))   
           
     #def event(self, event):
    #    if event.type() == QtCore.QEvent.WindowActivate:
    #        self.select_data("") 
    #    return QtWidgets.QWidget.event(self, event)

    def closeEvent(self, event):
        # Закрытие окна и выход из приложения (чтобы не возвращаться в LoginWindow)
        #print("close Window - закрывается программа") 
        sys.exit(app.exec_())
       
if __name__ == '__main__':
    # Инициализация таблиц базы данных (сделать один раз)
    database.init_db() 
    #exit(0)
    # Создаются объекты application и MainWindow. 
    app = QApplication(sys.argv)
    # Стили
    #file = QtCore.QFile("styles.qss")                              
    file = QtCore.QFile("SimpleStyles.qss")                              
    #file = QtCore.QFile("MyMaterialDark.qss")                              
    file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
    stream = QtCore.QTextStream(file)
    app.setStyleSheet(stream.readAll())
    #main_window = MainWindow()
    # Создаются дочерние окна
    login_window = LoginWindow()            
    # Показать окно
    login_window.show()
    #main_window.show()
    # Запускается основной цикл.
    sys.exit(app.exec_())
        
