"""
Демоснтрация процессов работы с данными в
сравнении с https://opendatabim.io/index.php/data-handling-in-construction/

IFC спецификация, на которую ориентируемся: https://standards.buildingsmart.org/IFC/RELEASE/IFC4_1/FINAL/HTML/
"""
import ifcopenshell as _ifc
import pandas as pd
from _general import mguu_cource_tools

ifc_file = _ifc.open(
    r'C:\Users\Georg\Documents\GitHub\PyIfcOpenShell_cource\DataExamples\rme_advanced_sample_project.ifc')

def get_object_properties(ifc_entity):
    temp_props = {"IfcClass": ifc_entity.is_a(), "GlobalId": ifc_entity.GlobalId}
    ifc_props_root = ifc_entity.IsDefinedBy
    for props_group in ifc_props_root:
        if props_group.is_a("IfcRelDefinesByProperties"):
            props_definition = props_group.RelatingPropertyDefinition

            def get_prop_data(props_array):
                for ps in props_array:
                    p_name = ps.Name

                    # print(p_name)

                    def check_prop(check_value):
                        if check_value is not None:
                            if isinstance(check_value, (int, float, bool, str)):
                                temp_props[p_name] = check_value
                            else:
                                d_new = check_value.get_info()
                                for k2, v2 in d_new.items():
                                    check_prop(v2)
                        pass

                    for k1, v1 in ps.get_info().items():
                        check_prop(v1)
                pass

            # property sets
            if props_definition.is_a("IfcPropertySet"):
                get_prop_data(props_definition.HasProperties)
            # qto
            if props_definition.is_a("IfcElementQuantity"):
                get_prop_data(props_definition.Quantities)
    return temp_props
"""
Подсчет значений свойств (входящих в список needing_prop_sum_names), для элементов чье свойство с именем 
ObjectType содержит слова из спсика needing_names

ВНИМАНИЕ!!!!
Не все САПР выгружают категорию в прицнипе в файл IFC. В данном случае это тег ObjectType, 
но в других случаях он может быть другой!
"""


def getting_summa_of_prop_by_category(needing_category_names, needing_prop_sum_names):
    ifc_objects = ifc_file.by_type("IfcObject")
    ifc_objects_new = list((filter(lambda x: x.is_a() in needing_category_names, ifc_objects)))
    out_dict = {"Object name" : [], "Total value": []}
    for ifc_entity in ifc_objects_new:
        #print(ifc_entity.get_info())
        entity_name = ifc_entity.ObjectType
        temp_props = get_object_properties(ifc_entity)
        # calc_values
        for k, v in temp_props.items():
            if k in needing_prop_sum_names:
                if entity_name not in out_dict["Object name"]:
                    out_dict["Object name"].append(entity_name)
                    out_dict["Total value"].append(v)
                else:
                    index_that_name = out_dict["Object name"].index(entity_name)
                    out_dict["Total value"][index_that_name] += v
                break
    #print(str(out_dict))
    df = pd.DataFrame(data=out_dict, columns=out_dict.keys())
    return df


import openpyxl
ifc_summa_info = getting_summa_of_prop_by_category(["IfcWall", "IfcWallStandardCase"], ["Volumen", "NetVolume", "Volume"])
ifc_summa_info.to_excel(r'C:\Users\Georg\Documents\GitHub\PyIfcOpenShell_cource\DataExamples\test_summa.xlsx')
