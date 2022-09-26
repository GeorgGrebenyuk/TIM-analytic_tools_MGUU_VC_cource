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

class mguu_cource_tools:
    """
    Получение файлового пути к примеру файла модели с проверкой его существования.
    В противном случае возврат None
    """
    @staticmethod
    def get_example_file_path (ex_file_name):
        file_dir = os.path.dirname(__file__)
        ifc_file_path = os.path.join(file_dir , '../DataExamples/' + ex_file_name)
        ifc_file_path = os.path.abspath(os.path.realpath(ifc_file_path))
        if os.path.exists(ifc_file_path):
            return ifc_file_path
        else:
            return None
    """
    Преобразование GUID в UUID
    """
    @staticmethod
    def convert_uuid_to_guid (guid_input):
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
        ifc_file_path = os.path.join(file_dir , '../DataExamples/UsersCreated/' + filename)
        ifc_file_path = os.path.abspath(os.path.realpath(ifc_file_path))
        with open(ifc_file_path, "w") as f:
            f.write(template)
            f.close()
        return ifc_file_path

    @staticmethod
    #Создание уникального идентификатора (UUID) для новых элементов
    def create_guid():
        return ifcopenshell.guid.compress(uuid.uuid1().hex)

    #Получение объектных свойств из сущности
    @staticmethod
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
    
    #Получение словаря по уровням со значением свойства по его имени
    @staticmethod
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