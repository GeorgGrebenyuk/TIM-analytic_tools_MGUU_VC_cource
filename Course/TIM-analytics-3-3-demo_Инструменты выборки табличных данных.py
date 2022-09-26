"""
Курс "ТИМ-ориентированная аналитика. Современные инструменты работа с данными"

Блок 3 - Работа с табличными данными в Python (библиотека pandas)
Официальная справка см. здесь - https://pandas.pydata.org/docs/user_guide/index.html

Урок: Dataframe pandas, инструменты выборки данных в таблицах
Материал по теме: https://habr.com/ru/company/ruvds/blog/494720/, https://habr.com/ru/post/196980/,
https://habr.com/ru/post/197212/, https://python-scripts.com/plot-with-pandas
"""
from _general import mguu_cource_tools
import pandas as pd

import numpy as np

excel_path = mguu_cource_tools.get_example_file_path("UsersCreated/15d83007-3da4-11ed-8b83-e0d4e8d2be27.xlsx")
pd_dataframe = pd.read_excel(excel_path, usecols= "B:G")
#print(pd_dataframe)

#Получение датафрейма только для объемных элементов без графы count
df_without_count_column = pd_dataframe.drop("Count", axis =1)
df_objects_volume = df_without_count_column[df_without_count_column["Net Volume"] > 0]
#print(df_objects_volume)

#Получение датафрейма для точечных элементов без графы Net Volume
df_without_volume_column = pd_dataframe.drop("Net Volume", axis =1)
df_objects_count = df_without_count_column[df_without_count_column["Net Volume"] < 0]
#print(df_objects_count)

#Получение суммарного объема для Ifc классов по уровням
df_summa_volume_by_storey = pd.pivot_table(df_objects_volume, index = "Level_name", columns = "IfcClass",
                                           values = "Net Volume", aggfunc=np.sum, fill_value=0)
print(df_summa_volume_by_storey)

#Получение суммарного количества классов по уровням
df_summa_count_by_storey = pd.pivot_table(pd_dataframe, index="IfcClass", columns = "Level_name",
                                          values="Count", aggfunc=np.sum, fill_value=0)