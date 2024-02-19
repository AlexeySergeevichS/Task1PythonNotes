""" Задание
Реализовать консольное приложение заметки, с сохранением, чтением,
добавлением, редактированием и удалением заметок. Заметка должна
содержать идентификатор, заголовок, тело заметки и дату/время создания или
последнего изменения заметки. Сохранение заметок необходимо сделать в
формате json или csv формат (разделение полей рекомендуется делать через
точку с запятой). Реализацию пользовательского интерфейса студент может
делать как ему удобнее, можно делать как параметры запуска программы
(команда, данные), можно делать как запрос команды с консоли и
последующим вводом данных, как-то ещё, на усмотрение студента """

from csv import DictReader, DictWriter
import datetime
import pandas as pd
from os.path import exists
from dateutil import parser

note_id_name = 'Идентификатор'
note_header_name = 'Заголовок'
note_text_name = 'Тело'
note_date_name = 'Дата'
delim = ';'

# вводим заголовок и текст заметки, возвращаем их с текущей датой
def get_new_info():
    is_valid = False
    header = None
    while not is_valid:
        header = input('Введи заголовок: ')
        if len(header) == 0:
            print('Пустой ввод!')
        else:
            is_valid = True
    is_valid = False
    note_text = None
    while not is_valid:
        note_text = input('Введи текст заметки: ')
        if len(note_text) == 0:
            print('Пустой ввод!')
        else:
            is_valid = True
    return [header, note_text, datetime.datetime.now().strftime('%d-%m-%Y')]

# создает новый файл с именем и с полями
def create_file(file_name):
    with open(file_name, 'w', encoding='utf-8') as data:
        file_writer = DictWriter(
            data, delimiter=delim, fieldnames=[note_id_name, note_header_name, note_text_name, note_date_name])
        file_writer.writeheader()

# запись в файл данных из lst
def write_file(lst, file_name):
    res = read_file(file_name)
    # добавляем новую строку
    res.append({note_id_name: len(res) + 1, note_header_name: lst[0],
                note_text_name: lst[1], note_date_name: lst[2]})
    file_write(file_name, res)

# запись после редактирования
def edit_file(id, lst, file_name):
    res = read_file(file_name)
    # меняем отредактированную строку
    res[id][note_header_name] = lst[0]
    res[id][note_text_name] = lst[1]
    res[id][note_date_name] = lst[2]
    # перезаписываем файл
    file_write(file_name, res)

# удаляем указанную заметку
def del_in_file(id, file_name):
    res = read_file(file_name)
    res.pop(id)
    # перезаписываем файл
    file_write(file_name, res)

# запись в файл
def file_write(file_name, res):
    with open(file_name, 'w', encoding='utf-8', newline='') as data:
        file_writer = DictWriter(
            data, delimiter=delim, fieldnames=[note_id_name, note_header_name, note_text_name, note_date_name])
        file_writer.writeheader()
        file_writer.writerows(res)

# читаем весь файл и возвращаем list словарей
def read_file(f_name):
    with open(f_name, 'r', encoding='utf-8') as data:
        f_reader = DictReader(data, delimiter=delim)
        return list(f_reader)

# фильтрация по дате
def filter(f_name, start_date, end_date):
    df = pd.read_csv(f_name, sep=delim)
    df[note_date_name] = pd.to_datetime(df[note_date_name])
    filtered_df = df[(df[note_date_name] >= start_date ) & (df[note_date_name] <= end_date)]
    print(filtered_df)

# вывод заметки по id
def find_some_rows(some_id, f_name):
    if not exists(f_name):
        print('Нет файла!')
        return
    lst = read_file(f_name)
    res = []
    for k, v in lst[some_id].items():
        res.append(v)
    return res

def main():
    file_name = input('Ведите имя файла справочника без расширения: ')
    if len(file_name) == 0:
        file_name = 'notes.csv'
        print('Пустое имя файла. Будет использовано имя по умолчанию(' + file_name + ').')
    else:
        file_name = file_name + '.csv'
    while True:
        command = input('Введите команду (список команд - help ): ').lower()
        if command == 'q':
            break
        elif command == 'add':
            if not exists(file_name):
                create_file(file_name)
            write_file(get_new_info(), file_name)
            print('Заметка добавлена!')
        elif command == 'readall':
            if not exists(file_name):
                print('Нет файла!')
                continue
            print(*read_file(file_name))
        elif command == 'read':
            while True:
                command = input(
                    'Введите номер заметки(всего заметок ' + str(len(read_file(file_name))) + ', b - вернуться обратно): ').lower()
                if command == 'b':
                    break
                elif command.isnumeric():
                    if (int(command) > 0) and (int(command) < (len(read_file(file_name)) + 1)):
                        print(*find_some_rows(int(command)-1, file_name))
                    else:
                        print('Неверная команда!')
                        break
                else:
                    print('Неверная команда!')
                    continue
        elif command == 'edit':
            while True:
                command = input(
                    'Введите номер заметки для редактирования(всего заметок ' + str(len(read_file(file_name))) + ', b - вернуться обратно): ').lower()
                if command == 'b':
                    break
                elif command.isnumeric():
                    if (int(command) > 0) and (int(command) < (len(read_file(file_name)) + 1)):
                        edit_file(int(command) - 1, get_new_info(), file_name)
                        print('Заметка сохранена!')
                    else:
                        print('Неверная команда!')
                        break
                else:
                    print('Неверная команда!')
                    continue
        elif command == 'del':
            while True:
                command = input(
                    'Введите номер заметки для удаления(всего заметок ' + str(len(read_file(file_name))) + ', b - вернуться обратно): ').lower()
                if command == 'b':
                    break
                elif command.isnumeric():
                    if (int(command) > 0) and (int(command) < (len(read_file(file_name)) + 1)):
                        del_in_file(int(command) - 1, file_name)
                        print('Заметка удалена!')
                    else:
                        print('Неверная команда!')
                        break
                else:
                    print('Неверная команда!')
                    continue
        elif command == 'filter':
             while True:
                command = input(
                        'Введите начальную дату в формате dd-mm-yyyy, (b - вернуться обратно): ').lower()
                if command == 'b':
                    break
                try:
                    #start_date =  datetime.datetime.strptime(command, '%d-%m-%y')
                    start_date = parser.parse(command)
                except   ValueError:
                    print('Некорректная дата!')
                    continue  
                while True:
                    command = input(
                        'Введите конечную дату в формате dd-mm-yyyy, (b - вернуться обратно): ').lower()
                    if command == 'b':
                        break
                    try:
                        # end_date = datetime.datetime.strptime(command, '%d-%m-%y')
                        end_date = parser.parse(command)
                        filter(file_name, start_date, end_date)
                        break
                    except ValueError:
                        print('Некорректная дата!')
                        continue  
        elif command == 'clear':
            create_file(file_name)
        elif command == 'help':
            print('Команды:')
            print('q - выход')
            print('add - добавить заметку в файл')
            print('del - удалить заметку')
            print('edit - редактировать заметку')
            print('read - прочитать заметку')
            print('readall - вывести все заметки')
            print('filter - фильтр по дате')
            print('clear - очистить текущий файл заметок')
        else:
            print('Неверная команда!')
            continue
main()