"""
Демоснтрация процессов работы с данными в
сравнении с https://opendatabim.io/index.php/data-handling-in-construction/

IFC спецификация, на которую ориентируемся: https://standards.buildingsmart.org/IFC/RELEASE/IFC4_1/FINAL/HTML/
"""
import ifcopenshell as _ifc
import pandas as pd
from _general import mguu_cource_tools

"""
Получение супер-таблицы объектных свойств
"""


def getting_super_table_by_ifc(ifc_file_path):
    ifc_file = _ifc.open(ifc_file_path)
    ifc_objects = ifc_file.by_type("IfcObject")
    list_temp = list()
    total_props_names = list()
    for ifc_entity in ifc_objects:
        temp_props = mguu_cource_tools.get_object_properties(ifc_entity)
        list_temp.append(temp_props)
        # merge props
        current_names = temp_props.keys()
        for key in current_names:
            if key not in total_props_names:
                total_props_names.append(key)
    out_data = dict()
    for key in total_props_names:
        out_data[key] = []
    for entity_data in list_temp:
        for pr in total_props_names:
            if pr in entity_data.keys():
                out_data[pr].append(entity_data[pr])
            else:
                out_data[pr].append(None)
    df = pd.DataFrame(data=out_data, columns=total_props_names)
    return df


ifc_objects_data = getting_super_table_by_ifc(
    r'C:\Users\Georg\Documents\GitHub\PyIfcOpenShell_cource\DataExamples\rme_advanced_sample_project.ifc')
#для записи в excel
import openpyxl
print("start record")
ifc_objects_data.to_excel(r'C:\Users\Georg\Documents\GitHub\PyIfcOpenShell_cource\DataExamples\rme_advanced_sample_project_super_table.xlsx')
