"""
Курс "ТИМ-ориентированная аналитика. Современные инструменты работа с данными"

Общие настройки и инструменты (не изменять)
"""
from msilib import UuidCreate
import os
import uuid
import ifcopenshell
import time
import tempfile
import xml.etree.ElementTree as _xml


class mguu_cource_tools:
    """
    Получение файлового пути к примеру файла модели с проверкой его существования.
    В противном случае возврат None
    """

    @staticmethod
    def get_example_file_path(ex_file_name):
        file_dir = os.path.dirname(__file__)
        ifc_file_path = os.path.join(file_dir, '../DataExamples/' + ex_file_name)
        ifc_file_path = os.path.abspath(os.path.realpath(ifc_file_path))
        if os.path.exists(ifc_file_path):
            return ifc_file_path
        else:
            return None

    """
    Преобразование GUID в UUID
    """

    @staticmethod
    def convert_uuid_to_guid(guid_input):
        expanded = uuid.UUID('{' + str(guid_input) + '}')
        compressed = ifcopenshell.guid.compress(expanded.hex)
        return compressed

    """
    Преобразование UUID в GUID (?)
    """

    @staticmethod
    def __convert_guid_to_uuid(uuid_input):
        uuid_object = uuid.UUID(uuid_input)
        return ifcopenshell.guid.expand(uuid_object)

    """
    Создание IFC файла из шаблона и возврат файлового пути к нему
    """

    @staticmethod
    def create_ifc_by_template():
        # IFC template creation
        uuid_random = UuidCreate()
        filename = uuid_random + ".ifc"
        timestamp = time.time()
        timestring = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(timestamp))
        creator = "-"
        organization = "MGUU"
        application, application_version = "IfcOpenShell", "0.7.0"
        project_globalid, project_name = UuidCreate(), "Hello, Ifc"

        # A template IFC file to quickly populate entity instances for an IfcProject with its dependencies
        template = """ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('ViewDefinition [CoordinationView]'),'2;1');
FILE_NAME('%(filename)s','%(timestring)s',('%(creator)s'),('%(organization)s'),'%(application)s','%(application)s','');
FILE_SCHEMA(('IFC2X3'));
ENDSEC;
DATA;
#1=IFCPERSON($,$,'%(creator)s',$,$,$,$,$);
#2=IFCORGANIZATION($,'%(organization)s',$,$,$);
#3=IFCPERSONANDORGANIZATION(#1,#2,$);
#4=IFCAPPLICATION(#2,'%(application_version)s','%(application)s','');
#5=IFCOWNERHISTORY(#3,#4,$,.ADDED.,$,#3,#4,%(timestamp)s);
#6=IFCDIRECTION((1.,0.,0.));
#7=IFCDIRECTION((0.,0.,1.));
#8=IFCCARTESIANPOINT((0.,0.,0.));
#9=IFCAXIS2PLACEMENT3D(#8,#7,#6);
#10=IFCDIRECTION((0.,1.,0.));
#11=IFCGEOMETRICREPRESENTATIONCONTEXT($,'Model',3,1.E-05,#9,#10);
#12=IFCDIMENSIONALEXPONENTS(0,0,0,0,0,0,0);
#13=IFCSIUNIT(\*,.LENGTHUNIT.,$,.METRE.);
#14=IFCSIUNIT(\*,.AREAUNIT.,$,.SQUARE_METRE.);
#15=IFCSIUNIT(\*,.VOLUMEUNIT.,$,.CUBIC_METRE.);
#16=IFCSIUNIT(\*,.PLANEANGLEUNIT.,$,.RADIAN.);
#17=IFCMEASUREWITHUNIT(IFCPLANEANGLEMEASURE(0.017453292519943295),#16);
#18=IFCCONVERSIONBASEDUNIT(#12,.PLANEANGLEUNIT.,'DEGREE',#17);
#19=IFCUNITASSIGNMENT((#13,#14,#15,#18));
#20=IFCPROJECT('%(project_globalid)s',#5,'%(project_name)s',$,$,$,$,(#11),#19);
ENDSEC;
END-ISO-10303-21;
""" % locals()

        # Write the template to a temporary file 
        file_dir = os.path.dirname(__file__)
        ifc_file_path = os.path.join(file_dir, '../DataExamples/UsersCreated/' + filename)
        ifc_file_path = os.path.abspath(os.path.realpath(ifc_file_path))
        with open(ifc_file_path, "w") as f:
            f.write(template)
            f.close()
        return ifc_file_path

    @staticmethod
    # Создание уникального идентификатора (UUID) для новых элементов
    def create_guid():
        return ifcopenshell.guid.compress(uuid.uuid1().hex)

    # Получение объектных свойств из сущности
    @staticmethod
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
                                elif isinstance(check_value, (tuple, list)):
                                    ...
                                else:
                                    try:
                                        d_new = check_value.get_info()
                                    except():
                                        print(check_value)
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

        # Получение словаря по уровням со значением свойства по его имени

    @staticmethod
    def get_info_by_storeys_of_class(ifcfile, ifc_class_name, property_name):
        out_info = dict()
        ifc_storeys = ifcfile.by_type("IfcBuildingStorey")
        ifc_storeys.sort(key=lambda a: a.Name)
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

    # Получение триангуляции поверхности из Landxml файла для PostgreSQL - TIN Z
    @staticmethod
    def get_pgsql_tin_by_landxml_surface(surface_as_xml):
        ns_xmlns = "{http://www.landxml.org/schema/LandXML-1.2}"
        surface_as_xml = surface_as_xml.find(ns_xmlns + "Definition")
        pnts_block = surface_as_xml.find(ns_xmlns + "Pnts")
        pnts_collection_xml = pnts_block.findall(ns_xmlns + "P")
        pnts_collection = dict()
        for point_xml in pnts_collection_xml:
            p_number = point_xml.attrib["id"]
            p_coords = point_xml.text.split(' ')
            # Инвертируем очередность координат из-за спецификации LandXML
            pnts_collection[p_number] = str(p_coords[1]) + " " + str(p_coords[0]) + " " + str(p_coords[2])
        faces_block = surface_as_xml.find(ns_xmlns + "Faces")
        faces_collection_xml = faces_block.findall(ns_xmlns + "F")
        triangles_definition = list()
        for face_xml in faces_collection_xml:
            triangle_definition_points = list()
            points_indexes = face_xml.text.split(' ')
            points_indexes.append(points_indexes[0])
            for point_index in points_indexes:
                p_coord = pnts_collection[point_index]
                triangle_definition_points.append(p_coord)
            triangle_definition_temp = "((" + ",".join(triangle_definition_points) + "))"
            triangles_definition.append(triangle_definition_temp)
        result_tinz_definition = "TIN Z (" + ",".join(triangles_definition) + ")"
        return result_tinz_definition

    # Функция записи табличного представления данных в файл
    @staticmethod
    def write_to_file(save_name_file, table_to_record):
        file_dir = os.path.dirname(__file__)
        save_path = os.path.join(file_dir, '../DataExamples/UsersCreated/' + save_name_file + ".txt")
        save_path = os.path.abspath(os.path.realpath(save_path))
        with open(save_path, "w", encoding="utf8") as _file:
            for table_row in table_to_record:
                temp_table_row_string = '|'.join(str(row_element) for row_element in table_row)
                _file.write(temp_table_row_string + "\n")
        pass
