# Импорт библиотек
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
# Подключаем модуль для работы с датой/временем
from datetime import datetime
# Подключаем модуль для работы с БД
import database
# Модуль hashlib реализует общий интерфейс для множества различных безопасных алгоритмов хеширования и дайджеста сообщений
import hashlib
# Подключаем сообщения
from messages import msg

# Изменение пользователя
# Создается новый класс ChangePolzovatelWindow который наследуется от класса QMainWindow. 
class ChangePolzovatelWindow(QMainWindow):
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
            #checkAction = QAction(QIcon("check.png"), msg.save, self)
            #stopAction = QAction(QIcon("stop.png"), msg.cancel, self)
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
            self.label_login = QLabel(msg.login)
            self.label_password = QLabel(msg.password)
            #self.label_admin = QLabel(msg.admin)
            #self.label_manager = QLabel(msg.manager)
            # Поля ввода данных
            self.lineEdit_login = QLineEdit(self)
            self.lineEdit_password = QLineEdit(self)
            self.lineEdit_password.setEchoMode(QLineEdit.Password)
            self.checkBox_admin = QCheckBox(msg.admin, self)
            self.checkBox_manager = QCheckBox(msg.manager, self)
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
            grid_layout.addWidget(self.label_login, 0, 0, 1, 1)
            grid_layout.addWidget(self.lineEdit_login, 0, 1, 1, 3)             
            grid_layout.addWidget(self.label_password, 1, 0, 1, 1)
            grid_layout.addWidget(self.lineEdit_password, 1, 1, 1, 3) 
            grid_layout.addWidget(self.checkBox_admin, 2, 0, 1, 4) 
            grid_layout.addWidget(self.checkBox_manager, 3, 0, 1, 4) 
            grid_layout.addWidget(self.pushButtonUpdate, 4, 0, 1, 2) 
            grid_layout.addWidget(self.pushButtonCancel, 4, 2, 1, 2) 
            # Если это изменение записи, то загрузить ее иначе установка начальных значений и сокрытие поля пароль
            if self.record_id!=0:
                self.read_record()  
                self.lineEdit_login.setReadOnly(True)
                self.label_password.setVisible(False)
                self.lineEdit_password.setVisible(False)
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
            sql = "SELECT id, login, parol, administrator, menedzher FROM polzovatel WHERE id=" + str(self.record_id)
            # Получить результат запроса из resultSet можно с помощью методов, например, fetchall() или fetchone()   
            results = database.fetchOne(sql)
            self.lineEdit_login.setText(results[1])
            self.lineEdit_password.setText(str(results[2]))
            self.checkBox_admin.setChecked(results[3])
            self.checkBox_manager.setChecked(results[4])
        except Exception as error:
            print(error)
            QMessageBox.critical(self,  "Error",  str(error))   

    def update_data(self):
        try:
            # Данные
            login = self.lineEdit_login.text()
            parol = self.lineEdit_password.text()
            administrator = self.checkBox_admin.isChecked()
            menedzher = self.checkBox_manager.isChecked()
            # Проверка данных
            if login == "" or parol == "" :
                # Окно с информационным сообщением. Первая строка отображается в заголовке окна, вторая - в сообщении.
                QMessageBox.warning(self,  msg.warning,  msg.fill_all_fields)
                return     
            if len(login) < 4:
                QMessageBox.warning(self,  msg.warning,  msg.minimum_login_length_4_characters)
                return     
            if len(parol) < 4:
                QMessageBox.warning(self,  msg.warning,  msg.minimum_password_length_4_characters)
                return     
            # Изменение данных
            parol = hashlib.sha256(self.lineEdit_password.text().encode('utf-8')).hexdigest()            
            # SQL-запрос новая запись или изменение записи
            if self.record_id==0:
                sql = "INSERT INTO polzovatel  (login, parol, administrator, menedzher) VALUES (?, ?, ?, ?)"
            else:
                #sql = "UPDATE polzovatel SET login=? , parol=?, administrator=?, menedzher=? WHERE id=?"
                sql = "UPDATE polzovatel SET administrator=?, menedzher=? WHERE id=?"
            #print(sql)
            # Параметры запроса
            if self.record_id==0:
                parameters = [login, parol, administrator, menedzher]
            else:
                parameters = [administrator, menedzher]
                parameters.append(self.record_id)
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

# Создается новый класс PolzovatelListWindow котрый наследуется от класса QMainWindow. 
class PolzovatelListWindow(QMainWindow):
    def __init__(self):
        try:
            super().__init__()
            # Метод setGeometry() помещает окно на экране и устанавливает его размер.
            # Первые два параметра х и у - это позиция окна. Третий - ширина, и четвертый - высота окна.
            self.setGeometry(200, 200, 800, 600)
            # Заголовок окна
            self.setWindowTitle(msg.polzovateli)
            #self.setWindowIcon(QtGui.QIcon('logo.png'))
            self.setWindowIcon(QtGui.QIcon(':/images/logo.png'))
            # Создаём таблицу
            self.tableWidget = QTableWidget(self)  
            # Разные цвета для четных и нечетных строк
            self.tableWidget.setAlternatingRowColors(True);
            # Запрет изменения таблицы
            self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            # Устанавливаем количество колонок
            self.tableWidget.setColumnCount(4)
            # Устанавливаем заголовки таблицы
            self.tableWidget.setHorizontalHeaderLabels([msg.id, msg.login, msg.admin, msg.manager])
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
            self.pushButtonResetPassword = QPushButton(msg.reset)
            self.pushButtonResetPassword.setObjectName("pushButtonResetPassword")            
            self.pushButtonResetPassword.clicked.connect(lambda: self.reset_password())
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
            grid_layout.addWidget(self.tableWidget, 1, 0, 1, 6)                 
            grid_layout.addWidget(self.pushButtonInsert, 2, 0, 1, 1)            
            grid_layout.addWidget(self.pushButtonEdit, 2, 1, 1, 1)            
            grid_layout.addWidget(self.pushButtonResetPassword, 2, 2, 1, 1)            
            grid_layout.addWidget(self.pushButtonDelete, 2, 3, 1, 1)            
            grid_layout.addWidget(self.pushButtonRefresh, 2, 4, 1, 1)            
            grid_layout.addWidget(self.pushButtonExit, 2, 5, 1, 1)            
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
            # SQL-запрос
            sql = "SELECT id, login, administrator, menedzher FROM polzovatel " + where
            # Получить результат запроса из resultSet можно с помощью методов, например, fetchall() или fetchone()
            result = database.fetchAll(sql)
            # Установить количество строк
            self.tableWidget.setRowCount(0)
            self.tableWidget.setRowCount(len(result))
            # Установить количество строк
            self.tableWidget.setRowCount(0)
            self.tableWidget.setRowCount(len(result))
            # Заполнить таблицу
            #for i, elem in enumerate(result):
            #    for j, val in enumerate(elem):
            #        self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))  
            # Заполнить таблицу
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    if val == True and (j==2 or j==3):
                        self.tableWidget.setItem(i, j, QTableWidgetItem('✓'))  
                    elif val == False and (j==2 or j==3):
                        self.tableWidget.setItem(i, j, QTableWidgetItem(''))  
                    else:
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
            where = " WHERE login Like '%" +  self.lineEdit.text() + "%'"
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
            title = self.tableWidget.item(self.tableWidget.currentRow(), 1).text()
            # Окно с сообщением и с двумя кнопками: Yes и No. Первая строка отображается в заголовке окна.
            # Вторая строка является текстовым сообщением и отображается в диалоговом окне.
            # Третий аргумент определяет комбинацию кнопок, появляющихся в диалоге.
            # Последний параметр - кнопка по умолчанию. Это кнопка, на которой изначально установлен фокус клавиатуры. Возвращаемое значение хранится в переменной reply.
            reply = QMessageBox.question(self, msg.delete,  msg.delete_entry + "\n" + title + "?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            # Проверка возвращаемого значения
            if reply == QMessageBox.Yes:
                # Удаление записи SQL-запрос                 
                sql = "DELETE FROM polzovatel WHERE id=?"
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
            self.change_polzovatel_window = ChangePolzovatelWindow(0)
            self.change_polzovatel_window.setWindowTitle(msg.add)
            self.change_polzovatel_window.show()
        except Exception as error:
            print(error)
            QMessageBox.critical(self,  "Error",  str(error))   

    def edit_data(self):
        try:
            # Получение значения 0 ячейки текущей строки
            _id = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
            # Вызов дочернего окна для изменения записи
            self.change_polzovatel_window = ChangePolzovatelWindow(_id)  
            self.change_polzovatel_window.setWindowTitle(msg.change)
            self.change_polzovatel_window.show()   
        except Exception as error:
            print(error)
            QMessageBox.critical(self,  "Error",  str(error))   
    
    def reset_password(self):
        try:
            # Установить фокус
            self.tableWidget.setFocus()
            # Получение значения выделенной ячейки QTableWidget
            firstColValue: QTableWidgetItem = self.tableWidget.selectedItems()[0]
            # Получение значения 0 столбца ячейки текущей строки (фактически id записи)
            _id = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
            # Получение значения 1 ячейки текущей строки
            title = self.tableWidget.item(self.tableWidget.currentRow(), 1).text()
            # Окно с сообщением и с двумя кнопками: Yes и No. Первая строка отображается в заголовке окна.
            # Вторая строка является текстовым сообщением и отображается в диалоговом окне.
            # Третий аргумент определяет комбинацию кнопок, появляющихся в диалоге.
            # Последний параметр - кнопка по умолчанию. Это кнопка, на которой изначально установлен фокус клавиатуры. Возвращаемое значение хранится в переменной reply.
            reply = QMessageBox.question(self, msg.reset,  msg.reset_password + "\n" + title + "?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            # Проверка возвращаемого значения
            if reply == QMessageBox.Yes:
               # Пароль такой же как и логин
                parol = hashlib.sha256(title.encode('utf-8')).hexdigest()
                # SQL-запрос новая запись или изменение записи
                sql = "UPDATE polzovatel SET parol=? WHERE id=?"                
                #print(sql)
                # Параметры запроса
                parameters = [parol, _id]                
                # Параметры запроса
                parameters = [_id]
                # Выполнить запрос sql c параметрами parameters
                database.executeSQL(sql, parameters)
                # Сообщение
                QMessageBox.information(self,  msg.reset_password,  msg.user_password + "\n" + title + "\n" + msg.equal_to_his_login) 
            # Обновить данные в таблице
            self.select_data("")              
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
