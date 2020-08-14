
from lxml import etree
from dqt.tools.tags.tag import LeafTag
from dqt.tools import graphs

class ResultBoxImageLeafTag(LeafTag):

    def __init__(self, gdocs, dataset_id):
        super().__init__(
            self.process_tag,
            etree.Element,
            gdocs,
            dataset_id
        )
        
        self.set_required_data_field('name')
        self.set_required_data_field('passedCount')
        self.set_required_data_field('failedCount')
        self.set_required_data_field('notAvailableCount')

    def process_tag(self, data):
        buffer = graphs.resource_result_box(data['passedCount'], data['failedCount'], data['notAvailableCount'])
        image_file_path = self.gdocs.add_image_file(buffer, 'resultBoxImage_%s.png' % data['name'])
        buffer.close()

        image_element = etree.Element(
            '{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}frame',
            attrib={
                # '{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name': 'fr1',
                '{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}name': image_file_path,
                '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}anchor-type': 'as-char',
                '{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}width': '6.0cm',
                '{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}height': '2.0cm',
                '{urn:oasis:names:tc:opendocument:xmlns:style:1.0}rel-width': '100%',
                '{urn:oasis:names:tc:opendocument:xmlns:style:1.0}rel-height': 'scale',
                '{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}z-index': '0',
            }
        )
        image_element.append(etree.Element(
            '{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}image',
            attrib={
                '{http://www.w3.org/1999/xlink}href': image_file_path,
                '{http://www.w3.org/1999/xlink}type': 'simple',
                '{http://www.w3.org/1999/xlink}show': 'embed',
                '{http://www.w3.org/1999/xlink}actuate': 'onLoad',
                '{urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0}mime-type': 'image/png',
            }

        ))
        wrapper_element = etree.Element(
            '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p',
            attrib={
                '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}style-name': 'P1'
            }
        )
        wrapper_element.append(image_element)
        return wrapper_element
