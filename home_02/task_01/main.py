import csv
import re


def get_data(file_names):
    headers = ['Изготовитель ОС', 'Название ОС', 'Код продукта', 'Тип системы']
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    for file_name in file_names:
        
        with open(file_name, 'r') as file:
            data = file.read()
            os_prod_list.append(re.search(r'\s{2,}.*$',re.search(r'Изготовитель ОС:.*', data).group()).group().strip())
            os_name_list.append(re.search(r'\s{2,}.*$',re.search(r'Название ОС:.*', data).group()).group().strip())
            os_code_list.append(re.search(r'\s{2,}.*$',re.search(r'Код продукта:.*', data).group()).group().strip())
            os_type_list.append(re.search(r'\s{2,}.*$',re.search(r'Тип системы:.*', data).group()).group().strip())
            
    main_data = [headers, os_prod_list, os_name_list, os_code_list, os_type_list]           
    return main_data

def write_to_csv(file_name): 
with open(file_name, 'w', encoding='utf-8') as csv_file:
        file_writer = csv.writer(csv_file)
        for line in get_data(['home_02/task_01/info_1.txt', 'home_02/task_01/info_2.txt', 'home_02/task_01/info_3.txt']):
            file_writer.writerow(line)
        
write_to_csv('home_02/task_01/result.csv')