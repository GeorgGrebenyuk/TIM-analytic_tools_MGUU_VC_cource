"""
Курс "ТИМ-ориентированная аналитика. Современные инструменты работа с данными"

Блок 2 - Работа с IFC и XML в Python
Официальная справка см. здесь - https://ifcopenshell.github.io/docs/python/html/index.html

Урок: Кейсы работы с ifc-файлами
Материал по теме: 

ДЕМОНСТРАЦИОННЫЙ
"""
from _general import mguu_cource_tools
import ifcopenshell as _ifc

import os

def get_info_by_storeys_of_class(ifcfile, ifc_class_name, property_name):
    out_info = dict()
    ifc_storeys = ifcfile.by_type("IfcBuildingStorey")
    ifc_storeys.sort(key= lambda a:a.Name)
    for one_storey in ifc_storeys:
        temp_prop_value = 0.0
        storey_objects = one_storey.ContainsElements[0].RelatedElements
        for storey_object in storey_objects:
            if storey_object.is_a(ifc_class_name):
                dict_props = mguu_cource_tools.get_object_properties(storey_object)
                prop_value = dict_props[property_name]
                temp_prop_value += prop_value
        out_info[one_storey.Name] = temp_prop_value
    return out_info


#ifc_file = _ifc.open(mguu_cource_tools.get_example_file_path('Renga_House.ifc'))
#dict_storeys_volume = get_info_by_storeys_of_class(ifc_file, "IfcSlab", "NetVolume")
#print(str(dict_storeys_volume))

#Перебор файлов в папке
root_path = "C:\\Users\\Georg\\Documents\\GitHub\\PyIfcOpenShell_cource\\DataExamples\\ProjectEvolution"
root_path_os = os.path.abspath(root_path)
files_ifc_list_temp = list()

all_files_temp = os.listdir(root_path_os)
for one_file in all_files_temp:
    #print(one_file)
    if one_file.endswith(".ifc"):
        #print(one_file)
        files_ifc_list_temp.append(os.path.join(root_path_os, one_file))

#Работаем с файлами
out_dict = dict()
for one_path in files_ifc_list_temp:
    print(one_path)
    ifc_file = _ifc.open(one_path)
    file_name = os.path.basename(one_path)
    props_info = get_info_by_storeys_of_class(ifc_file, "IfcSlab", "NetVolume")
    temp_summa_value = 0.0
    for k,v in props_info.items():
        temp_summa_value += v
    out_dict[file_name] = temp_summa_value
print(str(out_dict))

