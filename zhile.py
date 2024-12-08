# Импорт библиотек
from asyncio.windows_events import NULL
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
# Подключаем модуль для работы с датой/временем
from datetime import datetime
# Подключаем модуль для работы с БД
import database
# Для работы со временными файлами
import tempfile
# Подключаем сообщения
from messages import msg

# Создается новый класс ChangeZhileWindow который наследуется от класса QMainWindow. 
class ChangeZhileWindow(QMainWindow):
    def __init__(self, _id):
        try:
            super().__init__()
            # Если record_id = 0 это значит новая запись, иначе _id существующая запись и это ее id
            self.record_id = _id
            # Метод setGeometry() помещает окно на экране и устанавливает его размер.
            # Первые два параметра х и у - это позиция окна. Третий - ширина, и четвертый - высота окна.
            self.setGeometry(200, 200, 800, 600)
            # Заголовок окна
            self.setWindowTitle(msg.change)
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
            self.pushButtonUpdate.setObjectName("pushButtonUpdate")
            self.pushButtonUpdate.clicked.connect(lambda: self.update_data())
            self.pushButtonCancel = QPushButton(msg.cancel)
            self.pushButtonCancel.setObjectName("pushButtonCancel")
            self.pushButtonCancel.clicked.connect(lambda: self.close())
            # Метки
            self.label_tip = QLabel(msg.tip)
            self.label_komnata = QLabel(msg.komnata) 
            self.label_adres = QLabel(msg.adres)
            self.label_polshchad1 = QLabel(msg.polshchad1)
            self.label_polshchad2 = QLabel(msg.polshchad2)
            self.label_etazh = QLabel(msg.etazh)
            self.label_etazhnost = QLabel(msg.etazhnost)
            self.label_opisanie = QLabel(msg.opisanie)
            self.label_data = QLabel(msg.data)
            self.label_price = QLabel(msg.price)
            self.label_klient = QLabel(msg.prodavec)
            #self.label_aktiv = QLabel(msg.aktiv)
            # Поля ввода данных
            self.comboBox_tip = QComboBox(self)
            self.lineEdit_komnata = QLineEdit(self)
            self.lineEdit_adres = QLineEdit(self)
            self.lineEdit_polshchad1 = QLineEdit(self)
            self.lineEdit_polshchad2 = QLineEdit(self)
            self.lineEdit_etazh = QLineEdit(self)
            self.lineEdit_etazhnost = QLineEdit(self)
            #self.lineEdit_opisanie = QLineEdit(self)
            self.plainTextEdit_opisanie = QPlainTextEdit(self)
            self.plainTextEdit_opisanie.height = 10
            self.dateEdit_data = QtWidgets.QDateEdit(calendarPopup=True)
            self.dateEdit_data.setDisplayFormat("dd.MM.yyyy")
            self.dateEdit_data.setFixedWidth(100)
            self.lineEdit_price = QLineEdit(self)
            self.comboBox_klient = QComboBox(self)
            self.checkBox_aktiv = QCheckBox(msg.aktiv, self)
            # Создаём центральный виджет
            central_widget = QWidget(self)
            central_widget.setMaximumHeight(650)
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
            grid_layout.addWidget(self.label_tip, 0, 0, 1, 1)
            grid_layout.addWidget(self.comboBox_tip, 0, 1, 1, 3)                          
            grid_layout.addWidget(self.label_komnata, 1, 0, 1, 1)
            grid_layout.addWidget(self.lineEdit_komnata, 1, 1, 1, 3)            
            grid_layout.addWidget(self.label_adres, 2, 0, 1, 1)
            grid_layout.addWidget(self.lineEdit_adres, 2, 1, 1, 3)
            grid_layout.addWidget(self.label_polshchad1, 3, 0, 1, 1)
            grid_layout.addWidget(self.lineEdit_polshchad1, 3, 1, 1, 3)
            grid_layout.addWidget(self.label_polshchad2, 4, 0, 1, 1)
            grid_layout.addWidget(self.lineEdit_polshchad2, 4, 1, 1, 3)
            grid_layout.addWidget(self.label_etazh, 5, 0, 1, 1)
            grid_layout.addWidget(self.lineEdit_etazh, 5, 1, 1, 3)
            grid_layout.addWidget(self.label_etazhnost, 6, 0, 1, 1)
            grid_layout.addWidget(self.lineEdit_etazhnost, 6, 1, 1, 3)
            grid_layout.addWidget(self.label_opisanie, 7, 0, 1, 1)
            #grid_layout.addWidget(self.lineEdit_opisanie, 7, 1, 1, 3)
            grid_layout.addWidget(self.plainTextEdit_opisanie, 7, 1, 1, 3)
            grid_layout.addWidget(self.label_data, 8, 0, 1, 1)
            grid_layout.addWidget(self.dateEdit_data, 8, 1, 1, 3)
            grid_layout.addWidget(self.label_price, 9, 0, 1, 1)
            grid_layout.addWidget(self.lineEdit_price, 9, 1, 1, 3)
            grid_layout.addWidget(self.label_klient, 10, 0, 1, 1)
            grid_layout.addWidget(self.comboBox_klient, 10, 1, 1, 3)
            grid_layout.addWidget(self.checkBox_aktiv, 11, 1, 1, 4)
            grid_layout.addWidget(self.pushButtonUpdate, 12, 0, 1, 3) 
            grid_layout.addWidget(self.pushButtonCancel, 12, 3, 1, 3)  
            # Если это изменение записи, то загрузить ее иначе установка начальных значений
            if self.record_id!=0:
                self.read_record()        
            else:                
                # Заполнить combobox-ы
                sql = "SELECT id, nazvanie FROM tip ORDER BY nazvanie"
                # С помощью метода execute объекта cursor можно выполнить запрос в базу данных из Python. Он принимает SQLite-запрос в качестве параметра и возвращает resultSet (строки базы данных):                
                dictionary = database.fetchAll(sql)
                for row in dictionary:
                    self.comboBox_tip.addItem(row[1], row[0])                
                # Заполнить combobox-ы
                sql = "SELECT id, fio FROM klient ORDER BY fio"
                # С помощью метода execute объекта cursor можно выполнить запрос в базу данных из Python. Он принимает SQLite-запрос в качестве параметра и возвращает resultSet (строки базы данных):                
                dictionary = database.fetchAll(sql)
                for row in dictionary:
                    self.comboBox_klient.addItem(row[1], row[0])     
                # Установить текущую дату
                date = QDate.currentDate()
                self.dateEdit_data.setDate(date)
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
            sql = "SELECT id, tip_id, komnata, adres, polshchad1, polshchad2, etazh, etazhnost, opisanie, data, price, klient_id, aktiv FROM zhile WHERE id=" + str(self.record_id)
            # Получить результат запроса из resultSet можно с помощью методов, например, fetchall() или fetchone()   
            results = database.fetchOne(sql)
            self.lineEdit_komnata.setText(str(results[2]))                
            self.lineEdit_adres.setText(str(results[3]))                
            self.lineEdit_polshchad1.setText(str(results[4]))               
            self.lineEdit_polshchad2.setText(str(results[5]))               
            self.lineEdit_etazh.setText(str(results[6]))               
            self.lineEdit_etazhnost.setText(str(results[7]))  
            #self.lineEdit_opisanie.setText(str(results[8]))  
            self.plainTextEdit_opisanie.insertPlainText(str(results[8]))  
            qdate = QtCore.QDate.fromString(str(results[9])[0:10], "yyyy-MM-dd")              
            self.dateEdit_data.setDate(qdate)   
            self.lineEdit_price.setText(str(results[10]))  
            self.checkBox_aktiv.setChecked(results[12])
            # Заполнить combobox-ы
            sql = "SELECT id, nazvanie FROM tip ORDER BY nazvanie"
            dictionary = database.fetchAll(sql)
            j=0
            for row in dictionary:
                self.comboBox_tip.addItem(row[1], row[0])
                if results[1]==row[0]:
                    self.comboBox_tip.setCurrentIndex(j)
                j=j+1
             # Заполнить combobox-ы
            sql = "SELECT id, fio FROM klient ORDER BY fio"
            dictionary = database.fetchAll(sql)
            j=0
            for row in dictionary:
                self.comboBox_klient.addItem(row[1], row[0])
                if results[11]==row[0]:
                    self.comboBox_klient.setCurrentIndex(j)
                j=j+1
        except Exception as error:
            print(error)
            QMessageBox.critical(self,  "Error",  str(error))   

    def update_data(self):
        try:
            # Данные
            tip_id=self.comboBox_tip.itemData(self.comboBox_tip.currentIndex())
            komnata = self.lineEdit_komnata.text() 
            adres = self.lineEdit_adres.text()
            polshchad1 = self.lineEdit_polshchad1.text()
            polshchad2 = self.lineEdit_polshchad2.text()
            etazh = self.lineEdit_etazh.text()
            etazhnost = self.lineEdit_etazhnost.text()
            #opisanie = self.lineEdit_opisanie.text()
            opisanie = self.plainTextEdit_opisanie.toPlainText()
            data = self.dateEdit_data.date().toPyDate()
            price = self.lineEdit_price.text()
            klient_id=self.comboBox_klient.itemData(self.comboBox_klient.currentIndex())
            aktiv = self.checkBox_aktiv.isChecked()
            # Проверка данных
            if tip_id == 0 or komnata == "" or adres == "" or polshchad1 == "" or polshchad2 == "" or etazh == "" or etazhnost == "" or price == "" or klient_id == 0:
                # Окно с информационным сообщением. Первая строка отображается в заголовке окна, вторая - в сообщении.
                QMessageBox.warning(self,  msg.warning,  msg.fill_all_fields)
            # Изменение данных
            # SQL-запрос новая запись или изменение записи
            if self.record_id==0:
                sql = "INSERT INTO zhile (tip_id, komnata, adres, polshchad1, polshchad2, etazh, etazhnost, opisanie, data, price, klient_id, aktiv) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            else:
                sql = "UPDATE zhile SET tip_id=?, komnata=?, adres=?, polshchad1=?, polshchad2=?, etazh=?, etazhnost=?, opisanie=?, data=?, price=?, klient_id=?, aktiv=? WHERE id=?"
            #print(sql)
            # Параметры запроса
            parameters = [tip_id, komnata, adres, polshchad1, polshchad2, etazh, etazhnost, opisanie, data, price, klient_id, aktiv]
            if self.record_id != 0: 
                parameters.append(self.record_id)
            #print(parameters)
            # Выполнить запрос sql c параметрами parameters
            database.executeSQL(sql, parameters)
            # Закрыть окно
            self.close()
        except Exception as error:
            print(error)
            QMessageBox.critical(self,  "Error",  str(error))   

    #def closeEvent(self, event):        
    #    # Обновить данные в таблице при закрытии окна
    #    self.select_data("")

# Создается новый класс ZhileListWindow котрый наследуется от класса QMainWindow. 
class ZhileListWindow(QMainWindow):
    def __init__(self):
        try:
            super().__init__()
            # Метод setGeometry() помещает окно на экране и устанавливает его размер.
            # Первые два параметра х и у - это позиция окна. Третий - ширина, и четвертый - высота окна.
            self.setGeometry(200, 200, 800, 600)
            # Заголовок окна
            self.setWindowTitle(msg.zhile)
            #self.setWindowIcon(QtGui.QIcon('logo.png'))
            self.setWindowIcon(QtGui.QIcon(':/images/logo.png'))
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
            self.tableWidget.doubleClicked.connect(lambda: self.edit_data())
            # Устанавливаем выравнивание на заголовки
            """
            tableWidget.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
            tableWidget.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
            tableWidget.horizontalHeaderItem(2).setTextAlignment(Qt.AlignHCenter)
            tableWidget.horizontalHeaderItem(3).setTextAlignment(Qt.AlignHCenter)
            """            
            # Поле ввода строки поиска
            self.lineEdit = QLineEdit(self)            
            # Кнопка для поиска
            self.button = QPushButton(msg.filter)
            self.button.clicked.connect(lambda: self.filter_data())            
            ## Панели инструментов обеспечивают быстрый доступ к наиболее часто используемым командам.
            ## Создается действие с соответствующей иконкой.  
            #insertAction = QAction(QIcon(":/images/add.png"), msg.add, self)
            #editAction = QAction(QIcon(":/images/edit.png"), msg.edit, self)
            #deleteAction = QAction(QIcon(":/images/delete.png"), msg.delete, self)
            #refreshAction = QAction(QIcon(":/images/refresh.png"), msg.refresh, self)
            #exitAction = QAction(QIcon(":/images/exit.png"), msg.exit, self)
            ## Для этого действия определяется комбинация клавиш.
            #exitAction.setShortcut("Ctrl+Q")
            ##
            #insertAction.triggered.connect(lambda: self.insert_data())
            #editAction.triggered.connect(lambda: self.edit_data())
            #deleteAction.triggered.connect(lambda: self.delete_data())
            #refreshAction.triggered.connect(lambda: self.select_data(""))
            #exitAction.triggered.connect(lambda: self.close())
            ## Метод addToolBar() создает панель инструментов.
            ## Создается кнопка и к ней добавля.тся действие.
            #self.toolbar = self.addToolBar("Toolbar")
            #self.toolbar.setIconSize(QSize(32,32))
            #self.toolbar.addAction(insertAction)
            #self.toolbar.addAction(editAction)
            #self.toolbar.addAction(deleteAction)
            #self.toolbar.addAction(refreshAction)
            #self.toolbar.addAction(exitAction)
            # Кнопки
            self.pushButtonInsert = QPushButton(msg.add)
            self.pushButtonInsert.setObjectName("pushButtonInsert")
            self.pushButtonInsert.clicked.connect(lambda: self.insert_data())
            self.pushButtonEdit = QPushButton(msg.edit)
            self.pushButtonEdit.setObjectName("pushButtonEdit")            
            self.pushButtonEdit.clicked.connect(lambda: self.edit_data())
            self.pushButtonDelete = QPushButton(msg.delete)
            self.pushButtonDelete.setObjectName("pushButtonDelete")
            self.pushButtonDelete.clicked.connect(lambda: self.delete_data())
            self.pushButtonRefresh = QPushButton(msg.refresh)
            self.pushButtonRefresh.setObjectName("pushButtonRefresh")
            self.pushButtonRefresh.clicked.connect(lambda: self.select_data(""))
            self.pushButtonExit = QPushButton(msg.exit)
            self.pushButtonExit.setObjectName("pushButtonExit")
            self.pushButtonExit.clicked.connect(lambda: self.close())
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
            grid_layout.addWidget(self.lineEdit, 0, 0, 1, 2)
            grid_layout.addWidget(self.button, 0, 2, 1 , 1)
            # Ячейка начинается с первой строки и нулевой колонки, и занимает 1 строку и 5 колонок.
            grid_layout.addWidget(self.tableWidget, 1, 0, 1, 5)                 
            grid_layout.addWidget(self.pushButtonInsert, 2, 0, 1, 1)            
            grid_layout.addWidget(self.pushButtonEdit, 2, 1, 1, 1)            
            grid_layout.addWidget(self.pushButtonDelete, 2, 2, 1, 1)            
            grid_layout.addWidget(self.pushButtonRefresh, 2, 3, 1, 1)            
            grid_layout.addWidget(self.pushButtonExit, 2, 4, 1, 1)          
            # Выравнивание окна по центру
            # Класс QtWidgets.QDesktopWidget предоставляет информацию о компьютере пользователя, в том числе о размерах экрана. Получаем прямоугольник, определяющий геометрию главного окна. Это включает в себя любые рамки окна.
            qr = self.frameGeometry()
            # Получаем разрешение экрана монитора, и с этим разрешением, мы центральную точку
            cp = QDesktopWidget().availableGeometry().center()
            # Наш прямоугольник уже имеет ширину и высоту. Теперь мы установили центр прямоугольника в центре экрана. Размер прямоугольника не изменяется.
            qr.moveCenter(cp)
            # Двигаем верхний левый угол окна приложения в верхний левый угол прямоугольника qr, таким образом, центрируя окно на нашем экране.
            self.move(qr.topLeft())  
            # Обновить данные
            #self.select_data("")  
        except Exception as error:
            print(error)
            QMessageBox.critical(self,  "Error",  str(error))   

    def select_data(self, where):
        try:
            ## SQL-запрос
            sql = "SELECT id, tip, komnata, adres, polshchad1, polshchad2, etazh, etazhnost, strftime('%d.%m.%Y', data) AS data_, price, prodavec, aktiv FROM view_zhile " + where
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
            # Сброс строки поиска
            if where=="":
                self.lineEdit.setText("")
        except Exception as error:
            print(error)
            QMessageBox.critical(self,  "Error",  str(error))   

    def filter_data(self):
        try:
            # Сформировать строку поиска
            where = " WHERE adres Like '%" +  self.lineEdit.text() + "%'"
            # Обновить данные в таблице
            self.select_data(where)            
        except Exception as error:
            print(error)
            QMessageBox.critical(self,  "Error",  str(error))   

    def delete_data(self):
        try:
            # Установить фокус
            self.tableWidget.setFocus()
            # Получение значения выделенной ячейки QTableWidget
            firstColValue: QTableWidgetItem = self.tableWidget.selectedItems()[0]
            # Получение значения 0 столбца ячейки текущей строки (фактически id записи)
            _id = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
            # Получение значения 1 ячейки текущей строки
            adres = self.tableWidget.item(self.tableWidget.currentRow(), 1).text()
            # Окно с сообщением и с двумя кнопками: Yes и No. Первая строка отображается в заголовке окна.
            # Вторая строка является текстовым сообщением и отображается в диалоговом окне.
            # Третий аргумент определяет комбинацию кнопок, появляющихся в диалоге.
            # Последний параметр - кнопка по умолчанию. Это кнопка, на которой изначально установлен фокус клавиатуры. Возвращаемое значение хранится в переменной reply.
            reply = QMessageBox.question(self, msg.delete,  msg.delete_entry + "\n" + adres + "?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            # Проверка возвращаемого значения
            if reply == QMessageBox.Yes:
                # Удаление записи SQL-запрос                 
                sql = "DELETE FROM zhile WHERE id=?"
                # Параметры запроса
                parameters = [_id]
                # Выполнить запрос sql c параметрами parameters
                database.executeSQL(sql, parameters)
            # Обновить данные в таблице
            self.select_data("")              
        except Exception as error:
            print(error)
            QMessageBox.critical(self,  "Error",  str(error))   

    def insert_data(self):
        try:
            # Вызов дочернего окна для изменения записи
            self.change_zhile_window = ChangeZhileWindow(0)    
            self.change_zhile_window.setWindowTitle(msg.add)
            self.change_zhile_window.show()
        except Exception as error:
            print(error)
            QMessageBox.critical(self,  "Error",  str(error))   

    def edit_data(self):
        try:
            # Получение значения 0 ячейки текущей строки
            _id = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
            # Вызов дочернего окна для изменения записи
            self.change_zhile_window = ChangeZhileWindow(_id)   
            self.change_zhile_window.setWindowTitle(msg.change)
            self.change_zhile_window.show()   
        except Exception as error:
            print(error)
            QMessageBox.critical(self,  "Error",  str(error))   
    
    def event(self, event):
        if event.type() == QtCore.QEvent.WindowActivate:
            self.select_data("")  
            #print(f"Oкно стало активным; (WindowActivate).")
        #elif event.type() == QtCore.QEvent.WindowDeactivate:
        #    print(f"Oкно стало НЕактивным; (WindowDeactivate).") 
        #elif event.type() == QtCore.QEvent.Close:
        #    print(f"Oкно закрытo (QCloseEvent).") 
        return QtWidgets.QWidget.event(self, event)
