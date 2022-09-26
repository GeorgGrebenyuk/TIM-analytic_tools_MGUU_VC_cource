"""
Курс "ТИМ-ориентированная аналитика. Современные инструменты работа с данными"

Блок 2 - Работа с IFC и XML в Python
Официальная справка см. здесь - https://ifcopenshell.github.io/docs/python/html/index.html

Урок: Получение объектных данных (в том числе недокументированные методы)
Материал по теме: 

ДЕМОНСТРАЦИОННЫЙ
"""
from _general import mguu_cource_tools

#Импорт библиотеки для работы с IFC
import ifcopenshell as _ifc

def get_object_properties(ifc_entity):
    out_props = dict()
    #IfcRelDefinesByProperties
    ifc_props_root = ifc_entity.IsDefinedBy
    for props_group in ifc_props_root:
        #print(props_group)
        props_definition = props_group.RelatingPropertyDefinition
        if props_definition.is_a("IfcPropertySet"):
            #print("IfcPropertySet")
            for props_definition_prop in props_definition.HasProperties:
                #print(props_definition_prop)
                if props_definition_prop.is_a("IfcPropertySingleValue"):
                    out_props[props_definition_prop.Name] = props_definition_prop.NominalValue
                    #print(str(props_definition_prop.Name) + ' ' + str(props_definition_prop.NominalValue))
        elif props_definition.is_a("IfcElementQuantity"):
            #print("IfcElementQuantity")
            for one_quantity in props_definition.Quantities:
                #print(one_quantity)
                if one_quantity.is_a("IfcQuantityArea"):
                    out_props[one_quantity.Name] = one_quantity.AreaValue
                elif one_quantity.is_a("IfcQuantityCount"):
                    out_props[one_quantity.Name] = one_quantity.CountValue
                elif one_quantity.is_a("IfcQuantityLength"):
                    out_props[one_quantity.Name] = one_quantity.LengthValue
                elif one_quantity.is_a("IfcQuantityTime"):
                    out_props[one_quantity.Name] = one_quantity.TimeValue
                elif one_quantity.is_a("IfcQuantityVolume"):
                    out_props[one_quantity.Name] = one_quantity.VolumeValue
                elif one_quantity.is_a("IfcQuantityWeight"):
                    out_props[one_quantity.Name] = one_quantity.WeightValue
    return out_props 

def get_object_geometry (ifc_entity):
    object_Representation = ifc_entity.Representation
    print(object_Representation)
    if object_Representation.is_a("IfcProductDefinitionShape"):
        object_Representations = object_Representation.Representations
        for object_Representation_one in object_Representations:
            print(object_Representation_one)
            if object_Representation_one.is_a("IfcShapeRepresentation"):
                items = object_Representation_one.Items
                for item in items:
                    print(item)
                    if item.is_a("IfcMappedItem"):
                        shape = item.MappingSource.MappedRepresentation
                        print(shape)
                        for sub_item in shape.Items:
                            print(sub_item)
                            if sub_item.is_a("IfcFacetedBrep"):
                                for one_face in sub_item.Outer.CfsFaces:
                                    print(one_face.Bounds[0].Bound)
                                    for one_plg in one_face.Bounds[0].Bound.Polygon:
                                        print(one_plg)

ifc_file = _ifc.open(mguu_cource_tools.get_example_file_path('Renga_House.ifc'))
ifc_object_id = '3ZZpg7C_CNTUvpxzN75M8Y'
ifc_object = ifc_file.by_guid(ifc_object_id)
print(ifc_object)

get_object_geometry(ifc_object )
#object_props = get_object_properties(ifc_file, ifc_object)
#print(str(object_props ))