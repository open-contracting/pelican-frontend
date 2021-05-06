
from dqt.tools import graphs
from dqt.tools.elements import image_element
from dqt.tools.misc import terms_enumeration
from dqt.tools.tags.tag import LeafTag
from lxml import etree


class CountsResultBoxImageLeafTag(LeafTag):
    TYPES = set([
        'bar',
        # 'pie',
    ])

    def __init__(self, gdocs, dataset_id):
        super().__init__(
            self.process_tag,
            gdocs,
            dataset_id
        )

        self.set_param_validation(
            'type',
            lambda v: v in CountsResultBoxImageLeafTag.TYPES,
            description='The value must be one of the following: %s.' % terms_enumeration(CountsResultBoxImageLeafTag.TYPES)
        )

        self.set_required_data_field('name')
        self.set_required_data_field('counts_pairs')

    def process_tag(self, data):
        if self.get_param('type') is None or self.get_param('type') == 'bar':
            buffer, aspect_ratio = graphs.bar_result_box(data['counts_pairs'], return_aspect_ratio=True)
        elif self.get_param('type') == 'pie':
            # TODO
            raise NotImplemented()

        image_file_path = self.gdocs.add_image_file(buffer, 'resultBoxImage_%s.png' % data['name'])
        buffer.close()

        return image_element(image_file_path, aspect_ratio)
