import chardet
import re
import csv


def code_detecter(path):
    with open(path, 'rb') as fl:
        rawdata = fl.read()
        result = chardet.detect(rawdata)
        charenc = result['encoding']
        return charenc


list_of_files = ['info_1.txt', 'info_2.txt', 'info_3.txt']
need_to_search = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']

regexp = r': *(.*)\n'
os_prod_list, os_name_list, os_code_list, os_type_list = [], [], [], []
main_data = list()
main_data.append(need_to_search)


def get_data(path, regexp):
    with open(path, 'r', encoding=code_detecter(path)) as fl:
        data = fl.read()
        parameter_list = list()
        for idx, each in enumerate(need_to_search):
            match = re.findall(each + regexp, data)

            parameter_list.append(match[0])

            if idx == 0:
                os_prod_list.append(match[0])
            elif idx == 1:
                os_name_list.append(match[0])
            elif idx == 2:
                os_code_list.append(match[0])
            elif idx == 3:
                os_type_list.append(match[0])

        main_data.append(parameter_list)


def write_to_csv(path):
    for element in list_of_files:
        get_data(element, regexp)

    with open(path, 'w') as fl:
        writer = csv.writer(fl)
        for row in main_data:
            writer.writerow(row)


write_to_csv('final.csv')
