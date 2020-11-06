
from lxml import etree
from dqt.tools.tags.tag import LeafTag
from dqt.tools import graphs
from dqt.tools.misc import terms_enumeration
from dqt.tools.elements import image_element


class PassedResultBoxImageLeafTag(LeafTag):
    def __init__(self, gdocs, dataset_id):
        super().__init__(
            self.process_tag,
            gdocs,
            dataset_id
        )

        self.set_required_data_field('name')
        self.set_required_data_field('passedCount')
        self.set_required_data_field('failedCount')

    def process_tag(self, data):
        buffer, aspect_ratio = graphs.passed_result_box(
            data['passedCount'],
            data['failedCount'],
            return_aspect_ratio=True
        )
        image_file_path = self.gdocs.add_image_file(
            buffer,
            'resultBoxImage_%s_%s.png' % (self.get_param('level'), data['name'])
        )
        buffer.close()

        return image_element(image_file_path, aspect_ratio)
