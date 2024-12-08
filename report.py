# Импорт библиотек
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
# Подключаем модуль для работы с датой/временем
from datetime import datetime
# Подключаем модуль для работы с БД
import database
# Подключаем другие модули (инициализация, другие окна...)
import excel, html
# Подключаем сообщения
from messages import msg

class PrintHandler(QObject):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.m_page = None
        self.m_inPrintPreview = False

    def setPage(self, page):
        assert not self.m_page
        self.m_page = page
        self.m_page.printRequested.connect(self.printPreview)

    @pyqtSlot()
    def print(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self.m_page.view())
        if dialog.exec_() != QDialog.Accepted:
            return
        self.printDocument(printer)

    @pyqtSlot()
    def printPreview(self):
        if not self.m_page:
            return
        if self.m_inPrintPreview:
            return
        self.m_inPrintPreview = True
        printer = QPrinter()
        preview = QPrintPreviewDialog(printer, self.m_page.view())
        preview.paintRequested.connect(self.printDocument)
        preview.exec()
        self.m_inPrintPreview = False

    @pyqtSlot(QPrinter)
    def printDocument(self, printer):
        loop = QEventLoop()
        result = False

        def printPreview(success):
            nonlocal result
            result = success
            loop.quit()
        progressbar = QProgressDialog(self.m_page.view())
        progressbar.findChild(QProgressBar).setTextVisible(False)
        progressbar.setLabelText("Wait please...")
        progressbar.setRange(0, 0)
        progressbar.show()
        progressbar.canceled.connect(loop.quit)
        self.m_page.print(printer, printPreview)
        loop.exec_()
        progressbar.close()
        if not result:
            painter = QPainter()
            if painter.begin(printer):
                font = painter.font()
                font.setPixelSize(20)
                painter.setFont(font)
                painter.drawText(QPointF(10, 25), "Could not generate print preview.")
                painter.end()


# Создается новый класс ReportWindow котрый наследуется от класса QMainWindow. 
class ReportWindow(QMainWindow):
    def __init__(self):
        try:
            super().__init__()
            # Метод setGeometry() помещает окно на экране и устанавливает его размер.
            # Первые два параметра х и у - это позиция окна. Третий - ширина, и четвертый - высота окна.
            self.setGeometry(200, 200, 800, 600)
            # Заголовок окна
            self.setWindowTitle(msg.reports)    
            #self.setWindowIcon(QtGui.QIcon('logo.png'))
            self.setWindowIcon(QtGui.QIcon(':/images/logo.png'))
            # GroupBox выбора даты
            self.groupBox_date = QGroupBox(msg.data)
            self.groupBox_date.setMaximumHeight(60)
            self.grid_layout_date = QGridLayout()
            # Метки
            self.label_start = QLabel(msg.start)
            self.label_finish = QLabel(msg.finish)
            # Выбор даты
            self.dateEdit_start = QtWidgets.QDateEdit(calendarPopup=True)
            self.dateEdit_start.setDisplayFormat("dd.MM.yyyy")
            self.dateEdit_start.setFixedWidth(100)
            self.dateEdit_finish = QtWidgets.QDateEdit(calendarPopup=True)
            self.dateEdit_finish.setDisplayFormat("dd.MM.yyyy")
            self.dateEdit_finish.setFixedWidth(100) 
            # Добавляем  визуальные элементы в сетку
            self.grid_layout_date.addWidget(self.label_start, 0, 0, 1, 1)
            self.grid_layout_date.addWidget(self.dateEdit_start, 0, 1, 1, 2)
            self.grid_layout_date.addWidget(self.label_finish, 0, 3, 1, 1)
            self.grid_layout_date.addWidget(self.dateEdit_finish, 0, 4, 1, 2)
            self.groupBox_date.setLayout(self.grid_layout_date)
            ## GroupBox выбора условий
            #self.groupBox_condition = QGroupBox(msg.condition)
            #self.groupBox_condition.setMaximumHeight(85)
            #self.grid_layout_condition = QGridLayout()
            #self.groupBox_condition.setLayout(self.grid_layout_condition)
            ## Метки
            #self.label_otdel = QLabel(msg.otdel)
            #self.label_dolzhnost = QLabel(msg.dolzhnost)
            ## Элементы выбора
            #self.comboBox_otdel = QComboBox(self)
            #self.comboBox_otdel.addItem("Любой(-ое)", 0) 
            #self.comboBox_dolzhnost = QComboBox(self)
            #self.comboBox_dolzhnost.addItem("Любой(-ое)", 0) 
            ## Добавляем  визуальные элементы в сетку
            #self.grid_layout_condition.addWidget(self.label_otdel, 0, 0, 1, 1)
            #self.grid_layout_condition.addWidget(self.comboBox_otdel, 0, 2, 1, 3)
            #self.grid_layout_condition.addWidget(self.label_dolzhnost, 1, 0, 1, 1)
            #self.grid_layout_condition.addWidget(self.comboBox_dolzhnost, 1, 2, 1, 3)            
            ## Заполнить combobox-ы
            #sql = "SELECT id, nazvanie FROM otdel ORDER BY nazvanie"
            ## Получить результат запроса из resultSet можно с помощью методов, например, fetchall() или fetchone()
            #dictionary = database.fetchAll(sql)
            #for row in dictionary:
            #    self.comboBox_otdel.addItem(row[1], row[0]) 
            ## Заполнить combobox-ы
            #sql = "SELECT id, nazvanie FROM dolzhnost ORDER BY nazvanie"
            ## Получить результат запроса из resultSet можно с помощью методов, например, fetchall() или fetchone()
            #dictionary = database.fetchAll(sql)
            #for row in dictionary:
            #    self.comboBox_dolzhnost.addItem(row[1], row[0])                
            # GroupBox выбора отчета
            self.groupBox_report = QGroupBox(msg.report)
            self.groupBox_report.setMaximumHeight(110)
            self.grid_layout_report = QGridLayout()
            self.groupBox_report.setLayout(self.grid_layout_report)
            # Радиокнопки
            self.radioButtonReport1 = QRadioButton(msg.report1)
            self.radioButtonReport1.setChecked(True)
            self.radioButtonReport2 = QRadioButton(msg.report2)
            self.radioButtonReport3 = QRadioButton(msg.report3)
            self.radioButtonReport4 = QRadioButton(msg.report4)
            # Добавляем  визуальные элементы в сетку
            self.grid_layout_report.addWidget(self.radioButtonReport1, 0, 0, 1, 4)
            self.grid_layout_report.addWidget(self.radioButtonReport2, 1, 0, 1, 4)
            self.grid_layout_report.addWidget(self.radioButtonReport3, 2, 0, 1, 4)
            self.grid_layout_report.addWidget(self.radioButtonReport4, 3, 0, 1, 4)
            # Кнопки            
            self.pushButtonRun = QPushButton(msg.run)
            self.pushButtonRun.clicked.connect(lambda: self.run())
            self.pushButtonExit = QPushButton(msg.exit)
            self.pushButtonExit.clicked.connect(lambda: self.close())
            # CheckBox 
            self.checkBox_excel = QCheckBox(msg.export_to_excel)
            # Броузер
            self.browser = QWebEngineView()            
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
            #grid_layout.addWidget(self.groupBox_condition, 0, 0, 1, 4)
            grid_layout.addWidget(self.groupBox_report, 0, 0, 1, 4)            
            grid_layout.addWidget(self.groupBox_date, 1, 0, 1, 4)
            grid_layout.addWidget(self.checkBox_excel, 2, 0, 1, 2)      
            grid_layout.addWidget(self.pushButtonRun, 3, 1, 1, 1)                
            grid_layout.addWidget(self.pushButtonExit, 3, 2, 1, 1)      
            grid_layout.addWidget(self.browser, 4, 0, 1, 4)    
            # Выравнивание окна по центру
            # Класс QtWidgets.QDesktopWidget предоставляет информацию о компьютере пользователя, в том числе о размерах экрана. Получаем прямоугольник, определяющий геометрию главного окна. Это включает в себя любые рамки окна.
            qr = self.frameGeometry()
            # Получаем разрешение экрана монитора, и с этим разрешением, мы центральную точку
            cp = QDesktopWidget().availableGeometry().center()
            # Наш прямоугольник уже имеет ширину и высоту. Теперь мы установили центр прямоугольника в центре экрана. Размер прямоугольника не изменяется.
            qr.moveCenter(cp)
            # Двигаем верхний левый угол окна приложения в верхний левый угол прямоугольника qr, таким образом, центрируя окно на нашем экране.
            self.move(qr.topLeft())  
            # Установить диапазон дате "первое число года" - "текущая дата"
            date = QDate(QDate.currentDate().year(),  1, 1)
            self.dateEdit_start.setDate(date)
            self.dateEdit_finish.setDate(QDate.currentDate())
            # Обновить данные
            #self.select_data("")  
        except Exception as error:
            print(error)
            QMessageBox.critical(self,  "Error",  str(error))   

    def run(self):
        try:
            sql = ""
            header = []
            title = ""
            ## Предлжение Where
            #otdel_id=self.comboBox_otdel.itemData(self.comboBox_otdel.currentIndex())
            #dolzhnost_id=self.comboBox_dolzhnost.itemData(self.comboBox_dolzhnost.currentIndex())
            ##print(otdel_id)
            ##print(dolzhnost_id)
            #if otdel_id>0 or dolzhnost_id>0 :
            #    where = "WHERE "
            #    if otdel_id>0:
            #        where = where + " otdel='" + self.comboBox_otdel.currentText() + "' AND "
            #    if dolzhnost_id>0:
            #        where = where + " dolzhnost='" + self.comboBox_dolzhnost.currentText() + "' AND "
            #    where = where[:-4]
            #else:
            #    where = "WHERE id > 0"
            where = "WHERE id > 0"
            #print(where)
            # Условие
            if self.radioButtonReport1.isChecked() == True:
                # SQL-запрос чтения записи
                sql = '''SELECT id, tip, komnata, adres, polshchad1, polshchad2, etazh, etazhnost, opisanie, strftime('%d.%m.%Y', data) AS data_, price, prodavec 
                            FROM view_zhile 
                            WHERE aktiv = 1
                            ORDER BY data '''
                # Заголовок таблицы
                header = [msg.id, msg.tip, msg.komnata, msg.adres, msg.polshchad1, msg.polshchad2, msg.etazh, msg.etazhnost, 
                          msg.opisanie, msg.data, msg.price, msg.prodavec]
                # Название файла
                file_name = "sotrudnik.xls"
                # Заголовок отчета
                title = self.radioButtonReport1.text()
            # Условие
            if self.radioButtonReport2.isChecked() == True:
                sql = '''SELECT id, fio, adres, telefon FROM klient ORDER BY fio'''                
                header = [msg.id, msg.fio, msg.adres, msg.telefon]
                file_name = "klient.xls"
                # Заголовок отчета
                title = self.radioButtonReport2.text()
            # Условие
            if self.radioButtonReport3.isChecked() == True:
                #sql = "SELECT id, fio, adres, telefon, dolzhnost, (SELECT COUNT(*) FROM dogovor WHERE dogovor.sotrudnik_id=view_sotrudnik.id) AS kolvo, (SELECT SUM(price) FROM dogovor WHERE dogovor.sotrudnik_id=view_sotrudnik.id) AS summa "
                sql = "SELECT id, fio, adres, telefon, dolzhnost, "
                sql = sql + "(SELECT COUNT(*) FROM dogovor WHERE dogovor.sotrudnik_id=view_sotrudnik.id AND dogovor.data_dogovora>='" + str(self.dateEdit_start.date().toPyDate()) + "' AND dogovor.data_dogovora<='" + str(self.dateEdit_finish.date().toPyDate()) + "') AS kolvo,"
                sql = sql + "(SELECT SUM(price) FROM dogovor WHERE dogovor.sotrudnik_id=view_sotrudnik.id AND data_dogovora>='" + str(self.dateEdit_start.date().toPyDate()) + "' AND data_dogovora<='" + str(self.dateEdit_finish.date().toPyDate()) + "' ) AS summa "
                sql = sql + "FROM view_sotrudnik ORDER BY fio "
                #print(sql)
                header = [msg.id, msg.fio, msg.adres, msg.telefon, msg.dolzhnost, msg.kolvo + "<br>" + self.dateEdit_start.date().toPyDate().strftime('%d.%m.%Y') + "-" + self.dateEdit_finish.date().toPyDate().strftime('%d.%m.%Y') , msg.summa]
                file_name = "otpusk.xls"      
                # Заголовок отчета
                title = self.radioButtonReport3.text() 
            # Условие
            if self.radioButtonReport4.isChecked() == True:
                # SQL-запрос чтения записи
                sql = "SELECT id, strftime('%d.%m.%Y', data_dogovora) AS data_, nomer_dogovora, tip, komnata, adres, polshchad1, polshchad2, etazh, etazhnost, prodavec, pokupatel, price, sotrudnik FROM view_dogovor " 
                sql = sql + where + " AND data_dogovora>='" + str(self.dateEdit_start.date().toPyDate()) + "' AND data_dogovora<='" + str(self.dateEdit_finish.date().toPyDate()) + "' " 
                sql = sql + "ORDER BY data_dogovora, nomer_dogovora"                
                # Заголовок таблицы
                header = [msg.id, msg.data_dogovora, msg.nomer_dogovora, msg.tip, msg.komnata, msg.adres, msg.polshchad1, msg.polshchad2, 
                          msg.etazh, msg.etazhnost, msg.prodavec, msg.pokupatel, msg.price, msg.sotrudnik]
                # Название файла
                file_name = "sotrudnik.xls"
                # Заголовок отчета
                title = self.radioButtonReport4.text() + "<br>" + self.dateEdit_start.date().toPyDate().strftime('%d.%m.%Y') + "-" + self.dateEdit_finish.date().toPyDate().strftime('%d.%m.%Y') 
            # Получить результат запроса из resultSet можно с помощью методов, например, fetchall() или fetchone()
            data = database.fetchAll(sql)
            # Вывод в файл HTML, используется модуль html
            url = str("file:///" + html.export_to_html(title, header, data)).replace("\\", "/")
            #print(url)
            self.browser.setUrl(QUrl(url))
            #view = QWebEngineView()
            #view.setUrl(QUrl(url))
            #view.resize(1024, 750)
            #view.show()
            #self.browser.setUrl(QUrl(url))    
            #handler = PrintHandler()
            #handler.setPage(view.page())
            #printPreviewShortCut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_P), view)
            #printShortCut = QShortcut(QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_P), view)
            #printPreviewShortCut.activated.connect(handler.printPreview)
            #printShortCut.activated.connect(handler.print)
            
            # Вывод в Excel, используется модуль excel
            # Вызов: заголовок таблицы, данные, название файла
            # Окно с информационным сообщением. Первая строка отображается в заголовке окна, вторая - в сообщении.
            if self.checkBox_excel.isChecked():
                #QMessageBox.about(self,  msg.warning,  excel.export_to_excel(header, data, file_name))            
                excel.export_to_excel(header, data, file_name)
        except Exception as error:
            print(error)
            QMessageBox.critical(self,  "Error",  str(error))

    def event(self, event):
        #if event.type() == QtCore.QEvent.WindowActivate:
        #    self.select_data("")  
            #print(f"Oкно стало активным; (WindowActivate).")
        #elif event.type() == QtCore.QEvent.WindowDeactivate:
        #    print(f"Oкно стало НЕактивным; (WindowDeactivate).") 
        #elif event.type() == QtCore.QEvent.Close:
        #    print(f"Oкно закрытo (QCloseEvent).") 
        return QtWidgets.QWidget.event(self, event)
