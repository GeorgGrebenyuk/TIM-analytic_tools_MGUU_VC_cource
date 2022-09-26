"""
Курс "ТИМ-ориентированная аналитика. Современные инструменты работа с данными"

Блок 3 - Работа с табличными данными в Python (библиотека pandas)
Официальная справка см. здесь - https://pandas.pydata.org/docs/user_guide/index.html

Урок: чтение текстовых табличных файлов, преобразование таблиц в Dataframe
Материал по теме: https://habr.com/ru/company/ruvds/blog/494720/
"""
from _general import mguu_cource_tools
#Библиотека pandas
import pandas as pd

text_table_path = mguu_cource_tools.get_example_file_path("UsersCreated/15d83007-3da4-11ed-8b83-e0d4e8d2be27.txt")

def get_data_by_sm():
    file_data = list()
    with open(text_table_path, "r") as _file:
        for file_row in _file:
            file_data.append(file_row.split('|'))
    return file_data
    pass

#Работа с табличными даными в pandas
pd_dataframe = pd.read_table(text_table_path, sep = '|', encoding="utf8", header = 0)


excel_path = text_table_path.replace(".txt", ".xlsx")
pd_dataframe.to_excel(excel_path, sheet_name="Лист для данных")

pd_dataframe = pd.read_excel(excel_path, usecols= "B:G")
print(pd_dataframe)