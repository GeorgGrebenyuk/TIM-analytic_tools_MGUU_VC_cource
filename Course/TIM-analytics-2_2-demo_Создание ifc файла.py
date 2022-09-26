"""
Курс "ТИМ-ориентированная аналитика. Современные инструменты работа с данными"

Блок 2 - Работа с IFC и XML в Python
Официальная справка см. здесь - https://ifcopenshell.github.io/docs/python/html/index.html

Урок: Составление IFC-файла вручную
Оригинальный материал: https://academy.ifcopenshell.org/posts/creating-a-simple-wall-with-property-set-and-quantity-information/
ДЕМОНСТРАЦИОННЫЙ
"""
from _general import mguu_cource_tools

import ifcopenshell as _ifc

#Элементарная геометрия
Point_center = 0.0, 0.0, 0.0
Dir_x = 1.0, 0.0, 0.0
Dir_y = 0.0, 1.0, 0.0
Dir_z = 0.0, 0.0, 1.0

#Создание IfcAxis2Placement3D
def create_IfcAxis2Placement3D(point = Point_center, dir1 = Dir_z, dir2 = Dir_x):
    new_ifc_point = ifc_file.createIfcCartesianPoint(point)
    new_ifc_dir1 = ifc_file.createIfcDirection(dir1)
    new_ifc_dir2 = ifc_file.createIfcDirection(dir2)
    new_ifc_IfcAxis2Placement3D =  ifc_file.createIfcAxis2Placement3D(new_ifc_point, new_ifc_dir1, new_ifc_dir2)
    return new_ifc_IfcAxis2Placement3D

#Создание IfcLocalPlacement
def create_IfcLocalPlacement(point = Point_center, dir1 = Dir_z, dir2 = Dir_x, relative_to = None):
    aux_IfcAxis2Placement3D = create_IfcAxis2Placement3D(point, dir1, dir2)
    new_ifc_IfcLocalPlacement = ifc_file.createIfcLocalPlacement(relative_to, aux_IfcAxis2Placement3D)
    return new_ifc_IfcLocalPlacement

#Создание IfcRightCircularCylinder
def create_IfcRightCircularCylinder(object_IfcAxis2Placement3D, height, radius):
    new_ifc_IfcRightCircularCylinder = ifc_file.createIfcRightCircularCylinder(object_IfcAxis2Placement3D,height, radius )
    return new_ifc_IfcRightCircularCylinder

#Создание IfcRightCircularCone
def create_IfcRightCircularCone(object_IfcAxis2Placement3D, height, bottom_radius):
    new_ifc_IfcRightCircularCone = ifc_file.createIfcRightCircularCone(object_IfcAxis2Placement3D,height, bottom_radius )
    return new_ifc_IfcRightCircularCone

ifc_file_path = mguu_cource_tools.create_ifc_by_template()
global ifc_file
ifc_file = _ifc.open(ifc_file_path)

ifc_project = ifc_file.by_type("IfcProject")[0]
ifc_history = ifc_file.by_type("IfcOwnerHistory")[0]
ifc_context = ifc_file.by_type("IfcGeometricRepresentationContext")[0]

#Создание иерархии элементов
site_placement = create_IfcLocalPlacement()
ifc_site = ifc_file.createIfcSite(mguu_cource_tools.create_guid(),ifc_history, "Our Site", None, None, 
    site_placement, None, None, "ELEMENT", None, None, None, None, None)
ifc_building_placement = create_IfcLocalPlacement(relative_to=site_placement)
ifc_building = ifc_file.createIfcBuilding(mguu_cource_tools.create_guid(),ifc_history, "our Building", None, None, 
    ifc_building_placement, None, None, "ELEMENT", None, None, None )

ifc_building_storey_placament = create_IfcLocalPlacement(relative_to=ifc_building_placement)
ifc_building_storey = ifc_file.createIfcBuildingStorey(mguu_cource_tools.create_guid(),ifc_history, "our Storey", 
    None, None, ifc_building_storey_placament, None, None, "ELEMENT", 1.0)

#Создание геометрии объектов
wall_geometry_height = 6.0
wall_geometry_radius = 2.5

wall_length = 2*3.14159265 * wall_geometry_radius
wall_area = wall_geometry_height * wall_length
wall_volume = 3.14159265 * wall_geometry_radius * wall_geometry_radius * wall_geometry_height

wall_placement = create_IfcLocalPlacement(relative_to=ifc_building_storey_placament)
wall_geometry = create_IfcRightCircularCylinder(wall_placement, wall_geometry_height, wall_geometry_radius)
wall_representation = ifc_file.createIfcShapeRepresentation(ifc_context, "Body", "SolidModel", [wall_geometry])
wall_shape = ifc_file.createIfcProductDefinitionShape(None, None, [wall_representation])
wall_object = ifc_file.createIfcWallStandardCase(mguu_cource_tools.create_guid(),ifc_history, "our Wall", 
    None, None, wall_placement, wall_shape, None)

roof_placement = create_IfcLocalPlacement(point = (0.0, 0.0, wall_geometry_height), relative_to=ifc_building_storey_placament)
roof_geometry = create_IfcRightCircularCone(roof_placement, wall_geometry_height/2, wall_geometry_radius + 1.0)
roof_representation = ifc_file.createIfcShapeRepresentation(ifc_context, "Body", "SolidModel", [roof_geometry])
roof_shape = ifc_file.createIfcProductDefinitionShape(None, None, [roof_representation])
roof_object = ifc_file.createIfcRoof(mguu_cource_tools.create_guid(),ifc_history, "our Roof", 
    None, None, roof_placement, roof_shape, None)

#Работа со свойствами
props_list = [
    ifc_file.createIfcPropertySingleValue("Материал", "Наименование материала стены", ifc_file.create_entity("IfcText", "Кирпич"), None ),
    ifc_file.createIfcPropertySingleValue("Стоимость", "Стоимость возведения стены", ifc_file.create_entity("IfcReal", 1000.0), None )
]
property_set = ifc_file.createIfcpropertySet(mguu_cource_tools.create_guid(),ifc_history, "Наш набор свойств", None, props_list )
ifc_file.createIfcRelDefinesByProperties(mguu_cource_tools.create_guid(),ifc_history, None, None, [wall_object], property_set)

#Работа с расчетными характеристиками
quantity_list = [
    ifc_file.createIfcQuantityLength("Длина", "Длина стены", None, wall_length ),
    ifc_file.createIfcQuantityArea("Площадь", "Площадь наружной поверхности стены", None, wall_area),
    ifc_file.createIfcQuantityVolume("Объем", "Объем стены",  None, wall_volume)
]
quant_sets = ifc_file.createIfcElementQuantity(mguu_cource_tools.create_guid(),ifc_history, "Наш набор расчетных свойств", None,  None, quantity_list)
ifc_file.createIfcRelDefinesByProperties(mguu_cource_tools.create_guid(),ifc_history, None, None, [wall_object], quant_sets )

ifc_file.createIfcRelContainedInSpatialStructure(mguu_cource_tools.create_guid(),ifc_history, "our Wall", 
    None, [wall_object,roof_object], ifc_building_storey)

ifc_file.write(ifc_file_path)
print(ifc_project)