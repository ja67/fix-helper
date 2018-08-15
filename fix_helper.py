import os
import xml.etree.ElementTree as ET


class FixComponent(object):

    def __init__(self, number, value_hash=None):
        self.__number = number
        self.__value_hash = value_hash

    def __call__(self, *args, **kwargs):
        return self.__number

    def __str__(self):
        return self.__number

    def __repr__(self):
        return self.__number

    def __getattr__(self, item):
        if self.__value_hash:
            return self.__value_hash[item]
        raise AttributeError

    def get_value_hash(self):
        return [str(item) for item in self.__value_hash.keys()]


class FixComponentList(object):
    def __init__(self, version):
        self.__component_hash = self.__load_component_list(version)

    def __getattr__(self, item):
        return self.__component_hash[item]

    def get_component_hash(self):
        return [str(item) for item in self.__component_hash.keys()]

    def __load_component_list(self, version):
        fix_xml_tree = ET.parse(
            os.path.dirname(os.path.abspath(__file__)) + '/protocol_xml_files/FIX{}.xml'.format(version))
        fields_node_list = fix_xml_tree.getroot().find('fields').findall('field')
        result = {}
        for field_node in fields_node_list:
            value_hash = {
                value_node.get('description'): value_node.get('enum')
                for value_node in
                field_node.findall('value')
            }
            result[field_node.get('name')] = FixComponent(field_node.get('number'), value_hash)
        return result


version_list = ['40', '41', '42', '43', '44', '50', '50SP1', '50SP2', 'T11']
for version in version_list:
    globals()['FIX' + version] = FixComponentList(version)
