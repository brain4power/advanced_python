# 6. Создать текстовый файл test_file.txt, заполнить его тремя строками:
# «сетевое программирование», «сокет», «декоратор». Проверить кодировку файла по умолчанию.
# Принудительно открыть файл в формате Unicode и вывести его содержимое.

import chardet

PATH = 'test_file.txt'


def code_detecter(path):
    with open(path, 'rb') as fl:
        rawdata = fl.read()
        result = chardet.detect(rawdata)
        charenc = result['encoding']
        return charenc


print('Кодировка файла по умолчанию: ', code_detecter(PATH))

with open(PATH, 'r', encoding='utf') as fl:
    data = fl.read()
    print(data)
