# screen.py
# Вывод в HTML списка (списка списков)
# Для работы со временными файлами
import tempfile
# Экспорт данных в файл html
# header - Заголовок таблицы, data данные (список списков), название файла
def export_to_html(title, header, data):
    try:
        # Сохранить во временный файл
        #filename = tempfile.NamedTemporaryFile().name + ".html"
        filename = tempfile.gettempdir() + "\\report.html"
        #print(str(filename))
        f = open(filename, "w", encoding='utf-8')
        f.write("<html>" + "\n")
        f.write("<head>" + "\n")
        f.write("<meta charset=\"utf-8\">" + "\n")
        f.write("<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">" + "\n")
        f.write("</head>" + "\n")
        f.write("<body style=\"background-color: Cornsilk;color: Navy;\">" + "\n")
        f.write("<h2 style=\"text-align: left;\">" + title + "</h2>" + "\n")
        f.write("<table border=1>" + "\n")
        ## Заголовок
        f.write("<thead>" + "\n")
        f.write("<tr>" + "\n")
        for i in range(0, len(header)):        
            f.write("<th>" + header[i] + "</th>" + "\n")        
        f.write("</tr>" + "\n")
        f.write("</thead>" + "\n")
        # Данные
        f.write("<tbody>" + "\n")
        for row in data:
            f.write("<tr>" + "\n")
            for j in range(0, len(row)):
                if row[j] != None:
                    if str(type(row[j]))=="<class 'bytes'>":
                        # Сохранить во временный файл
                        fn = tempfile.gettempdir() + "\\" + str(row[0])
                        #fn = tempfile.NamedTemporaryFile().name
                        #print(fn)
                        with open(fn, 'wb') as file:
                            file.write(row[j])  
                        f.write("<td><img src='" + str(fn).replace("\\", "/") + "' alt='' style='height:100px; max-width:100px'/></td>" + "\n")                               
                    else:
                        f.write("<td>" + str(row[j]) + "</td>" + "\n")                    
                else:
                    f.write("<td></td>" + "\n")
            f.write("</tr>" + "\n")
        f.write("</tbody>" + "\n")
        f.write("</table>" + "\n")
        f.write("</body>" + "\n")
        f.write("</html>" + "\n")
        f.close()        
        # Вернуть имя файла
        return filename
    except Exception as e:
        message = "Сведения об ошибке: " + str(e)
        print(message)
        return message

