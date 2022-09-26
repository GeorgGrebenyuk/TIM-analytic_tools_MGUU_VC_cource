"""
Курс "ТИМ-ориентированная аналитика. Современные инструменты работа с данными"

Блок 3 - Работа с табличными данными в Python (библиотека pandas)
Официальная справка см. здесь - https://pandas.pydata.org/docs/user_guide/index.html

Урок: Подготовка текстовых файлов для анализа
Материал по теме: https://metanit.com/python/tutorial/4.2.php

ДЕМОНСТРАЦИОННЫЙ
"""
from _general import mguu_cource_tools
import ifcopenshell as _ifc


ifc_file = _ifc.open(mguu_cource_tools.get_example_file_path("L21-726-Родионова_108_А-ОВ-ВК.ifc"))

def get_objects_data():
    out_data_table = list()
    out_data_table.append(["Name", "IfcClass", "Level_name", "Net Volume", "Count", "GlobalId"])
    ifc_classes_volume = ["IfcWall", "IfcColumn", "IfcBeam", "IfcSlab"]
    ifc_classes_count = ["IfcWindow", "IfcDoor"]
    ifc_classes_permitted = ["IfcWall", "IfcColumn", "IfcBeam", "IfcSlab", "IfcWindow", "IfcDoor"]
    ifc_storeys = ifc_file.by_type("IfcBuildingStorey")
    for ifc_storey in ifc_storeys:
        storey_name = ifc_storey.Name
        ifc_entities = ifc_storey.ContainsElements[0].RelatedElements
        for ifc_entity in ifc_entities:
            if ifc_entity.is_a() in ifc_classes_permitted:
                volume_prop = 0.0
                count_prop = 1
                if ifc_entity.is_a() in ifc_classes_volume:
                    volume_prop = mguu_cource_tools.get_object_properties(ifc_entity)["NetVolume"]
                else:
                    volume_prop = -1
                out_data_table.append([
                    ifc_entity.Name,
                    ifc_entity.is_a(),
                    storey_name,
                    str(volume_prop),
                    str(count_prop),
                    ifc_entity.GlobalId])
    return out_data_table
    pass
def get_storeys_data():
    st_data = list()
    ifc_storeys = ifc_file.by_type("IfcBuildingStorey")
    for ifc_storey in ifc_storeys:
        st_data.append([ifc_storey.Name, ifc_storey.GlobalId, ifc_storey.Elevation])
    return st_data
    pass

def write_to_file(save_name_file, table_to_record):
    file_dir = os.path.dirname(__file__)
    save_path = os.path.join(file_dir, '../DataExamples/UsersCreated/' + save_name_file + ".txt")
    save_path = os.path.abspath(os.path.realpath(save_path))
    with open (save_path, "w", encoding = "utf8") as _file:
        for table_row in table_to_record:
            temp_table_row_string = '|'.join(str(row_element) for row_element in table_row)
            _file.write(temp_table_row_string + "\n")
    pass

import os
import uuid

#Наши действия
objects_data = get_objects_data()
write_to_file("objects_3d", objects_data)

storeys_data = get_storeys_data()
print()
write_to_file("storeys", storeys_data)
