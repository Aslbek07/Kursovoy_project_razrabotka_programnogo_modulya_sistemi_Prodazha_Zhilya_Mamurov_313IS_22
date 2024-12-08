# Вывод в excel списка (списка списков)
# Импорт библиотеки - https://pypi.org/project/xlwt/
from email import message
import xlwt
import os
# Экспорт данных в Excel
# header - Заголовок таблицы, data данные (список списков), название файла
def export_to_excel(header, data, file_name):
    try:
        # Максимальная ширина столбца в Excel
        col_max_width = 65535
        # Стиль заголовка
        style_header = xlwt.easyxf('font: name Arial, color-index blue, bold on')
        # Стиль данных
        style_data = xlwt.easyxf('font: name Arial')
        # Новая книга
        wb = xlwt.Workbook()
        # Новый лист
        ws = wb.add_sheet("List")
        # Заголовок
        for i in range(0, len(header)):        
            ws.write(0, i, header[i], style_header)
        # Номер строки (смещение на 1 строку из-за заголовка)
        i = 1
        for row in data:
            for j in range(0, len(row)):
                # Подбор ширины колонки в зависимости от длины выводимых данных
                cwidth = ws.col(j).width
                if (len(str(row[j]))*367) > cwidth:
                    if len(str(row[j]))*367 > col_max_width :
                        ws.col(j).width = col_max_width
                    else:
                        ws.col(j).width = (len(str(row[j]))*367)
                # Запись ячейки
                try:
                    ws.write(i, j, row[j], style_data)
                except Exception as e:
                    print(str(e))
            i = i + 1       # Увеличить счетчик строк
        # Сохранить книгу
        wb.save(file_name)
        # Открыть файл
        os.startfile(file_name)
        # Сообщение
        message = "См. файл: " + file_name
        print(message)
        return message
    except Exception as e:
        message = "Сведения об ошибке: " + str(e)
        print(message)
        return message
