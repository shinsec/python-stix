# Copyright (c) 2015, The MITRE Corporation. All rights reserved.
# See LICENSE.txt for complete terms.

# external
from lxml import etree
import mixbox.xml
from mixbox.vendor.six import BytesIO, iteritems

# internal
import stix
from stix.indicator.test_mechanism import _BaseTestMechanism
import stix.bindings.extensions.test_mechanism.open_ioc_2010 as open_ioc_tm_binding


@stix.register_extension
class OpenIOCTestMechanism(_BaseTestMechanism):
    _namespace = "http://stix.mitre.org/extensions/TestMechanism#OpenIOC2010-1"
    _binding = open_ioc_tm_binding
    _binding_class = _binding.OpenIOC2010TestMechanismType
    _xml_ns_prefix = "stix-openioc"
    _XSI_TYPE = "stix-openioc:OpenIOC2010TestMechanismType"
    _TAG_IOC = "{%s}ioc" % _namespace

    def __init__(self, id_=None, idref=None):
        super(OpenIOCTestMechanism, self).__init__(id_=id_, idref=idref)
        self.ioc = None
        self.__input_namespaces__ = {}
        self.__input_schemalocations__ = {}

    @property
    def ioc(self):
        return self._ioc
    
    @ioc.setter
    def ioc(self, value):
        if value is None:
            self._ioc = None
            return

        tree = mixbox.xml.get_etree(value)
        root = mixbox.xml.get_etree_root(tree)

        if root.tag != self._TAG_IOC:
            self._cast_ioc(root)

        self._collect_namespaces(root)
        self._collect_schemalocs(root)
        self._ioc = tree

    def _collect_schemalocs(self, node):
        try:
            schemaloc = mixbox.xml.get_schemaloc_pairs(node)
            self.__input_schemalocations__ = dict(schemaloc)
        except KeyError:
            self.__input_schemalocations__ = {}

    def _collect_namespaces(self, node):
        self.__input_namespaces__ = dict(iteritems(node.nsmap))

    def _cast_ioc(self, node):
        ns_ioc = "http://schemas.mandiant.com/2010/ioc"
        node_ns = etree.QName(node).namespace

        if node_ns == ns_ioc:
            etree.register_namespace(self._xml_ns_prefix, self._namespace)
            node.tag = self._TAG_IOC
        else:
            error = "Cannot set ioc. Expected tag '{0}' found '{1}'."
            error = error.format(self._TAG_IOC, node.tag)
            raise ValueError(error)

    @classmethod
    def from_obj(cls, obj, return_obj=None):
        if not obj:
            return None
        if not return_obj:
            return_obj = cls()
        
        super(OpenIOCTestMechanism, cls).from_obj(obj, return_obj)
        return_obj.ioc = obj.ioc
        return return_obj
    
    def to_obj(self, return_obj=None, ns_info=None):
        if not return_obj:
            return_obj = self._binding_class()
            
        super(OpenIOCTestMechanism, self).to_obj(return_obj=return_obj, ns_info=ns_info)
        return_obj.ioc = self.ioc
        return return_obj
    
    @classmethod
    def from_dict(cls, d, return_obj=None):
        if not d:
            return None
        if not return_obj:
            return_obj = cls()
            
        super(OpenIOCTestMechanism, cls).from_dict(d, return_obj)
        if 'ioc' in d:
            parser = mixbox.xml.get_xml_parser()
            return_obj.ioc = etree.parse(BytesIO(d['ioc']), parser=parser)
        
        return return_obj

    def to_dict(self):
        d = super(OpenIOCTestMechanism, self).to_dict()

        if self.ioc:
            d['ioc'] = etree.tostring(self.ioc)

        return d

