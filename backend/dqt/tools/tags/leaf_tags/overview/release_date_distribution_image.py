
import datetime

from lxml import etree
from dqt.tools.tags.tag import LeafTag
from dqt.tools import graphs
from dqt.tools.misc import parse_month_year


class ReleaseDateDistributionImageLeafTag(LeafTag):
    MONTH_YEAR_FORMAT = '%b-%-y'

    def __init__(self, gdocs, dataset_id):
        super().__init__(
            self.process_tag,
            gdocs,
            dataset_id
        )

        self.set_param_validation(
            'from',
            lambda v: parse_month_year(v) is not None,
            description='The value must be in the following format: <month>-<year> (e.g. Feb-19).'
        )
        self.set_param_validation(
            'to',
            lambda v: parse_month_year(v) is not None,
            description='The value must be in the following format: <month>-<year> (e.g. Feb-19).'
        )
        
        self.set_required_data_field('period_pairs')

    def process_tag(self, data):
        if self.get_param('from') is not None:
            from_d = parse_month_year(self.get_param('from'))
        else:
            from_d = datetime.datetime.min

        if self.get_param('to') is not None:
            to_d = parse_month_year(self.get_param('to'))
        else:
            to_d = datetime.datetime.max

        filter_period_pairs = []
        for period_str, count in data['period_pairs']:
            period_d = parse_month_year(period_str)
            if from_d <= period_d <= to_d:
                filter_period_pairs.append((period_str, count))

        buffer, aspect_ratio = graphs.histogram_result_box(
            filter_period_pairs,
            return_aspect_ratio=True
        )
        image_file_path = self.gdocs.add_image_file(
            buffer,
            'ReleaseDateDistributionImage.png'
        )
        buffer.close()

        image_element = etree.Element(
            '{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}frame',
            attrib={
                # '{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}style-name': 'fr1',
                '{urn:oasis:names:tc:opendocument:xmlns:drawing:1.0}name': image_file_path,
                '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}anchor-type': 'as-char',
                '{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}width': '6.0cm',
                '{urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0}height': '%fcm' % (6 * aspect_ratio),
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
        return image_element
