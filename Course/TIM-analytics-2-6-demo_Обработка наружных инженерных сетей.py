"""
Курс "ТИМ-ориентированная аналитика. Современные инструменты работа с данными"

Блок 2 - Работа с IFC и XML в Python (+Postgresql)
Официальная справка см. здесь - https://ifcopenshell.github.io/docs/python/html/index.html

Урок: Работа с XML, получение табличных данных и геометрии инженерных сетей и поверхности
Материал по теме:

ДЕМОНСТРАЦИОННЫЙ
"""
from _general import mguu_cource_tools
#Импрт библиотеки для xml

import xml.etree.ElementTree as _xml

#Требования к итоговым данным
table_surfaces = list()
table_surfaces.append(["Name", "Geometry"])
table_pipe_networks = list()
table_pipe_networks.append(["Name", "Description"])
table_structs = list()
table_structs.append(["Name", "Description", "Parent_networks", "Geometry"])
table_pipes = list()
table_pipes.append(["Name", "Description", "Parent_networks", "Diameter", "Thickness", "Geometry"])

xml_file = _xml.parse(mguu_cource_tools.get_example_file_path("Арх_данные.xml"))
ns_xmlns = "{http://www.landxml.org/schema/LandXML-1.2}"
xml_surfaces_block = xml_file.find(ns_xmlns + "Surfaces")
xml_surfaces_list = xml_surfaces_block.findall(ns_xmlns + "Surface")
for xml_surface in xml_surfaces_list:
    surface_name = xml_surface.attrib["name"]
    surface_geometry = mguu_cource_tools.get_pgsql_tin_by_landxml_surface(xml_surface)
    table_surfaces.append([surface_name, surface_geometry])
#начало обработки сетей
xml_pipe_networks_collection = xml_file.find(ns_xmlns + "PipeNetworks")
for xml_pipe_networks in xml_pipe_networks_collection:
    network_name = xml_pipe_networks.attrib["name"]
    table_pipe_networks.append([network_name, xml_pipe_networks.attrib["desc"]])
    #Колодцы
    temp_structs_for_pipes = dict()
    """
    key = Name of struct;
    value = dict():
        coord = x y
        elevation = z
        pipe_name_1 = pipe_z_1
        ...
        pipe_name_n = pipe_z_n
    """
    xml_structs_cillection = xml_pipe_networks.find(ns_xmlns + "Structs").findall(ns_xmlns + "Struct")
    for xml_struct in xml_structs_cillection:
        temp_struct_info = dict()
        temp_struct_info["elevation"] = xml_struct.attrib["elevRim"]
        struct_geometry_yx = xml_struct.find(ns_xmlns + "Center").text.split(" ")
        temp_struct_info["coord"] = str(struct_geometry_yx[1]) + " " + str(struct_geometry_yx[0])
        struct_geometry_xyz = "POINT Z (" +  temp_struct_info["coord"] + " " + temp_struct_info["elevation"] + ")"
        #смотрим трубы в/из колодца
        for pipe_in_struct in xml_struct.findall(ns_xmlns + "Invert"):
            temp_struct_info[pipe_in_struct.attrib["refPipe"]] = pipe_in_struct.attrib["elev"]
        temp_structs_for_pipes[xml_struct.attrib["name"]] = temp_struct_info
        table_structs.append([xml_struct.attrib["name"], xml_struct.attrib["desc"],
                              network_name, struct_geometry_xyz ])
    xml_pipes_collection = xml_pipe_networks.find(ns_xmlns + "Pipes").findall(ns_xmlns + "Pipe")
    for xml_pipe in xml_pipes_collection:
        try:
            pipe_name = xml_pipe.attrib["name"]
            pipe_circlepipe = xml_pipe.find(ns_xmlns + "CircPipe")
            #Получение колодцев связанных с трубой
            struct_start = temp_structs_for_pipes[xml_pipe.attrib["refStart"]]
            point_start = struct_start["coord"] + " " + struct_start[pipe_name]
            struct_end = temp_structs_for_pipes[xml_pipe.attrib["refEnd"]]
            point_end = struct_end["coord"] + " " + struct_end[pipe_name]
            line_pipe = "LINESTRING (" + point_start + ", " + point_end + ")"
            table_pipes.append([pipe_name, xml_pipe.attrib["desc"], network_name, pipe_circlepipe.attrib["diameter"],
                                pipe_circlepipe.attrib["thickness"],line_pipe])
        except:
            print(str(xml_pipe.attrib))

    #Запись в файл
mguu_cource_tools.write_to_file("ark_surfaces", table_surfaces)
mguu_cource_tools.write_to_file("ark_pipe_networks", table_pipe_networks)
mguu_cource_tools.write_to_file("ark_structs", table_structs)
mguu_cource_tools.write_to_file("ark_pipes", table_pipes)