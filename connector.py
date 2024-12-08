# Импорт библиотек
# Подключаем модуль для SQLite
import sqlite3

from PyQt5.QtWidgets import QMessageBox

# Создание соединения с базой данных с указанием конкретной схемы
def get_connection():
    try:
        conn = sqlite3.connect('db.sqlite3')
        return conn  
    except Exception as error:
        print(error)
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText(str(error))
        msg.setIcon(QMessageBox.Critical)
        msg.exec_()
