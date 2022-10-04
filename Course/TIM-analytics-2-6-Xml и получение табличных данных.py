"""
Курс "ТИМ-ориентированная аналитика. Современные инструменты работа с данными"

Блок 2 - Работа с IFC и XML в Python
Официальная справка см. здесь - https://ifcopenshell.github.io/docs/python/html/index.html

Урок: Работа с XML, получение табличных данных и геометрии сетей и поверхности
Материал по теме:

ДЕМОНСТРАЦИОННЫЙ
"""
from _general import mguu_cource_tools
#Импрт библиотеки для xml

import xml.etree.ElementTree as _xml

xml_file = _xml.parse(mguu_cource_tools.get_example_file_path("Арх_данные.xml"))
ns_xmlns = "{http://www.landxml.org/schema/LandXML-1.2}"
#Работа с поверхностями
table_surfaces = list()
table_surfaces.append(["Name", "Geometry"])
xml_surfaces_block = xml_file.find(ns_xmlns + "Surfaces")
xml_surfaces_list = xml_surfaces_block.findall(ns_xmlns + "Surface")
for xml_surface in xml_surfaces_list:
    surface_name = xml_surface.attrib["name"]
    pgsql_geometry = mguu_cource_tools.get_pgsql_tin_by_landxml_surface(xml_surface)
    table_surfaces.append([surface_name, pgsql_geometry])
    #print(pgsql_data)

#Работа с сетями

#Список систем
table_network = list()
table_network.append(["Name", "Description"])
#Список колодцев
table_structs = list()
table_structs.append(["Name", "Description", "Parent_Network", "Geometry"])
#Список труб
table_pipes = list()
table_pipes.append(["Name", "Description", "Parent_Network", "Diameter", "Thickness", "Geometry"])

pipe_networks_xml = xml_file.find(ns_xmlns + "PipeNetworks").findall(ns_xmlns + "PipeNetwork")
for pipe_network_xml in pipe_networks_xml:
    pipe_network_name = pipe_network_xml.attrib["name"]
    #Получаем свойства сети и заносим в таблицу
    table_network.append([pipe_network_name, pipe_network_xml.attrib["desc"]])
    #Получаем данные о колодцах
    """
    structs_info_for_pipes: временный словарь для последующего связывания труб с колодцами;
    Key = Name;
    Value = dict():
        coord = "x y"
        elevation = Z
        pipe_name1 = z1
        pipe_name2 = z2
        ...
        pipe_name_n = z_n
    """
    structs_info_for_pipes = dict()
    structs_collection_xml = pipe_network_xml.find(ns_xmlns + "Structs").findall(ns_xmlns + "Struct")
    for struct_xml in structs_collection_xml:
        struct_info_temp = dict()
        struct_info_temp["elevation"] = struct_xml.attrib["elevRim"]
        struct_geometry_xy = struct_xml.find(ns_xmlns + "Center").text.split(" ")
        struct_info_temp["coord"] = str(struct_geometry_xy[1]) + " " + str(struct_geometry_xy[0])
        struct_geometry_xyz = "POINT Z (" + struct_info_temp["coord"] + " " + struct_info_temp["elevation"] + ")"
        #parse connected pipes
        pipes_in_struct = struct_xml.findall(ns_xmlns + "Invert")
        for pipe_in_struct in pipes_in_struct:
            struct_info_temp[pipe_in_struct.attrib["refPipe"]] = p_z = pipe_in_struct.attrib["elev"]
        structs_info_for_pipes[struct_xml.attrib["name"]] = struct_info_temp
        table_structs.append([struct_xml.attrib["name"], struct_xml.attrib["desc"],
                              pipe_network_name, struct_geometry_xyz])
    #Получаем информацию о трубах
    #print(str(structs_info_for_pipes))
    pipes_collection_xml = pipe_network_xml.find(ns_xmlns + "Pipes").findall(ns_xmlns + "Pipe")
    for pipe_xml in pipes_collection_xml:
        try:
            pipe_name = pipe_xml.attrib["name"]
            pipe_circle = pipe_xml.find(ns_xmlns + "CircPipe")
            struct_start = structs_info_for_pipes[pipe_xml.attrib["refStart"]]
            #print(struct_start)
            point_start = struct_start["coord"] + " " + struct_start[pipe_name]
            struct_end = structs_info_for_pipes[pipe_xml.attrib["refEnd"]]
            #print(struct_end)
            point_end = struct_end["coord"] + " " + struct_start[pipe_name]
            line_geometry = "LINESTRING (" + point_start + ", " + point_end + ")"
            table_pipes.append([pipe_name, pipe_xml.attrib["desc"], pipe_network_name, pipe_circle.attrib["diameter"],
                                pipe_circle.attrib["thickness"], line_geometry])
        except:
            print(pipe_xml.attrib)

#Запись в файл
mguu_cource_tools.write_to_file("arch_pipe_network", table_network)
mguu_cource_tools.write_to_file("arch_pipes", table_pipes)
mguu_cource_tools.write_to_file("arch_structs", table_structs)
mguu_cource_tools.write_to_file("arch_surfaces", table_surfaces)