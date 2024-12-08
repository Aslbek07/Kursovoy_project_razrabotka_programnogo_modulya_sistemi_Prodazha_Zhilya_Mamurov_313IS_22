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

# Создается новый класс ChangeSotrudnikWindow который наследуется от класса QMainWindow. 
class ChangeSotrudnikWindow(QMainWindow):
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
            self.label_fio = QLabel(msg.fio)
            self.label_adres = QLabel(msg.adres) 
            self.label_telefon = QLabel(msg.telefon)
            self.label_dolzhnost = QLabel(msg.dolzhnost)
            # Поля ввода данных
            self.lineEdit_fio = QLineEdit(self)
            self.lineEdit_adres = QLineEdit(self)
            self.lineEdit_telefon = QLineEdit(self)
            #self.lineEdit_dolzhnost = QLineEdit(self)
            self.comboBox_dolzhnost = QComboBox(self)
            # Создаём центральный виджет
            central_widget = QWidget(self)
            central_widget.setMaximumHeight(250)
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
            grid_layout.addWidget(self.label_fio, 0, 0, 1, 1)
            grid_layout.addWidget(self.lineEdit_fio, 0, 1, 1, 3)                          
            grid_layout.addWidget(self.label_adres, 1, 0, 1, 1)
            grid_layout.addWidget(self.lineEdit_adres, 1, 1, 1, 3)            
            grid_layout.addWidget(self.label_telefon, 2, 0, 1, 1)
            grid_layout.addWidget(self.lineEdit_telefon, 2, 1, 1, 3)
            grid_layout.addWidget(self.label_dolzhnost, 3, 0, 1, 1)
            #grid_layout.addWidget(self.lineEdit_dolzhnost, 3, 1, 1, 3)
            grid_layout.addWidget(self.comboBox_dolzhnost, 3, 1, 1, 3)
            grid_layout.addWidget(self.pushButtonUpdate, 4, 0, 1, 3) 
            grid_layout.addWidget(self.pushButtonCancel, 4, 3, 1, 3)  
            # Если это изменение записи, то загрузить ее иначе установка начальных значений
            if self.record_id!=0:
                self.read_record()        
            else:                
                # Заполнить combobox-ы
                sql = "SELECT id, nazvanie FROM dolzhnost ORDER BY nazvanie"
                # С помощью метода execute объекта cursor можно выполнить запрос в базу данных из Python. Он принимает SQLite-запрос в качестве параметра и возвращает resultSet (строки базы данных):                
                dictionary = database.fetchAll(sql)
                for row in dictionary:
                    self.comboBox_dolzhnost.addItem(row[1], row[0])                
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
            sql = "SELECT id, fio, adres, telefon, dolzhnost_id FROM sotrudnik WHERE id=" + str(self.record_id)
            # Получить результат запроса из resultSet можно с помощью методов, например, fetchall() или fetchone()   
            results = database.fetchOne(sql)
            self.lineEdit_fio.setText(str(results[1]))                
            self.lineEdit_adres.setText(str(results[2]))                
            self.lineEdit_telefon.setText(str(results[3]))               
            # Заполнить combobox-ы
            sql = "SELECT id, nazvanie FROM dolzhnost ORDER BY nazvanie"
            dictionary = database.fetchAll(sql)
            j=0
            for row in dictionary:
                self.comboBox_dolzhnost.addItem(row[1], row[0])
                if results[4]==row[0]:
                    self.comboBox_dolzhnost.setCurrentIndex(j)
                j=j+1
        except Exception as error:
            print(error)
            QMessageBox.critical(self,  "Error",  str(error))   

    def update_data(self):
        try:
            # Данные
            fio = self.lineEdit_fio.text() 
            adres = self.lineEdit_adres.text()
            telefon = self.lineEdit_telefon.text()
            dolzhnost_id=self.comboBox_dolzhnost.itemData(self.comboBox_dolzhnost.currentIndex())
            # Проверка данных
            if fio == "" or adres == "" or telefon == "" or dolzhnost_id == 0:
                # Окно с информационным сообщением. Первая строка отображается в заголовке окна, вторая - в сообщении.
                QMessageBox.warning(self,  msg.warning,  msg.fill_all_fields)
            # Изменение данных
            # SQL-запрос новая запись или изменение записи
            if self.record_id==0:
                sql = "INSERT INTO sotrudnik (fio, adres, telefon, dolzhnost_id) VALUES (?, ?, ?, ?)"
            else:
                sql = "UPDATE sotrudnik SET fio=?, adres=?, telefon=?, dolzhnost_id=? WHERE id=?"
            #print(sql)
            # Параметры запроса
            parameters = [fio, adres, telefon, dolzhnost_id]
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

# Создается новый класс SotrudnikListWindow котрый наследуется от класса QMainWindow. 
class SotrudnikListWindow(QMainWindow):
    def __init__(self):
        try:
            super().__init__()
            # Метод setGeometry() помещает окно на экране и устанавливает его размер.
            # Первые два параметра х и у - это позиция окна. Третий - ширина, и четвертый - высота окна.
            self.setGeometry(200, 200, 800, 600)
            # Заголовок окна
            self.setWindowTitle(msg.sotrudniki)
            #self.setWindowIcon(QtGui.QIcon('logo.png'))
            self.setWindowIcon(QtGui.QIcon(':/images/logo.png'))
            # Создаём таблицу
            self.tableWidget = QTableWidget(self)  
            # Разные цвета для четных и нечетных строк
            self.tableWidget.setAlternatingRowColors(True);
            # Запрет изменения таблицы
            self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            # Устанавливаем количество колонок
            self.tableWidget.setColumnCount(5)
            # Устанавливаем заголовки таблицы
            self.tableWidget.setHorizontalHeaderLabels([msg.id, msg.fio, msg.adres, msg.telefon, msg.dolzhnost])
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
            sql = "SELECT id, fio, adres, telefon, dolzhnost FROM view_sotrudnik " + where
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
            where = " WHERE fio Like '%" +  self.lineEdit.text() + "%'"
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
                sql = "DELETE FROM sotrudnik WHERE id=?"
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
            self.change_sotrudnik_window = ChangeSotrudnikWindow(0)    
            self.change_sotrudnik_window.setWindowTitle(msg.add)
            self.change_sotrudnik_window.show()
        except Exception as error:
            print(error)
            QMessageBox.critical(self,  "Error",  str(error))   

    def edit_data(self):
        try:
            # Получение значения 0 ячейки текущей строки
            _id = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
            # Вызов дочернего окна для изменения записи
            self.change_sotrudnik_window = ChangeSotrudnikWindow(_id)   
            self.change_sotrudnik_window.setWindowTitle(msg.change)
            self.change_sotrudnik_window.show()   
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
