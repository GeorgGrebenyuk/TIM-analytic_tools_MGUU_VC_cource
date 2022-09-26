"""
Курс "ТИМ-ориентированная аналитика. Современные инструменты работа с данными"

Блок 2 - Работа с IFC и XML в Python
Официальная справка см. здесь - https://ifcopenshell.github.io/docs/python/html/index.html

Урок: Общие команды для работы с IFC
ДЕМОНСТРАЦИОННЫЙ
"""
from _general import mguu_cource_tools
import uuid
import ifcopenshell as _ifc

#by type
ifc_file = _ifc.open(mguu_cource_tools.get_example_file_path("Renga_House.ifc"))
ifc_project = ifc_file.by_type("IfcProject")[0]
#print(str(ifc_project.get_info()))
step_id = ifc_project.id()
#print("step_id = " + str(step_id))

#by_id
ifc_project = ifc_file.by_id(int(step_id))
#print(str(ifc_project.get_info()))

#by uuid
guid_old = '5bb660ae-654b-400c-8492-cecbfc1bdfc3'
uuid_ifc = mguu_cource_tools.convert_uuid_to_guid(guid_old)

ifc_project = ifc_file.by_guid(uuid_ifc)
#print(str(ifc_project.get_info()))


#Работа с окном и стеной
window_uuid = '1lG7A9IimhR$$PamwmLlhY'
ifc_window = ifc_file.by_guid(window_uuid)
print(ifc_window)

print("get_inverse")
elems_inverse = ifc_file.get_inverse(ifc_window)
for elem_inv in elems_inverse:
    print(elem_inv)

print("traverse")
elems_traverse = ifc_file.traverse(ifc_window, 3)
for elem_tr in elems_traverse:
    print(elem_tr)