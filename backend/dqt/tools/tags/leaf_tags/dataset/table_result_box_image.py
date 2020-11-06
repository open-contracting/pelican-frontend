
from lxml import etree
from dqt.tools.tags.tag import LeafTag
from dqt.tools import graphs
from dqt.tools.elements import image_element


class TableResultBoxImageLeafTag(LeafTag):

    def __init__(self, gdocs, dataset_id):
        super().__init__(
            self.process_tag,
            gdocs,
            dataset_id
        )

        self.set_required_data_field('name')
        self.set_required_data_field('counts_pairs')
        self.set_required_data_field('total_count')

    def process_tag(self, data):
        buffer, aspect_ratio = graphs.table_result_box(
            data['counts_pairs'],
            total_count=data['total_count'],
            return_aspect_ratio=True
        )

        image_file_path = self.gdocs.add_image_file(buffer, 'resultBoxImage_%s.png' % data['name'])
        buffer.close()

        return image_element(image_file_path, aspect_ratio)
