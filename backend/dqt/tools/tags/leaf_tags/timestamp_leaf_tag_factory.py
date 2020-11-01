
import datetime

from dqt.tools.tags.tag import LeafTag
from dqt.tools.misc import terms_enumeration

def generate_timestamp_leaf_tag(key, datetime_format):
    class TimestampLeafTag(LeafTag):
        MODES = set([
            'both',
            'date',
            'time',
        ])
        BOTH_DATETIME_FORMAT = '%Y-%m-%d %H.%M.%S'
        DATE_DATETIME_FORMAT = '%Y-%m-%d'
        TIME_DATETIME_FORMAT = '%H.%M.%S'

        def __init__(self, gdocs, dataset_id):
            super().__init__(
                self.process_tag,
                gdocs,
                dataset_id
            )
            
            self.set_param_validation(
                'mode',
                lambda v: v in TimestampLeafTag.MODES,
                description='The value must be one of the following: %s.' % terms_enumeration(TimestampLeafTag.MODES)
            )

            self.set_required_data_field(key)

        def process_tag(self, data):
            d = datetime.datetime.strptime(data[key], datetime_format)

            d_str = None
            if self.get_param('mode') == 'both' or self.get_param('mode') is None:
                d_str = d.strftime(TimestampLeafTag.BOTH_DATETIME_FORMAT)
            elif self.get_param('mode') == 'date':
                d_str = d.strftime(TimestampLeafTag.DATE_DATETIME_FORMAT)
            elif self.get_param('mode') == 'time':
                d_str = d.strftime(TimestampLeafTag.TIME_DATETIME_FORMAT)    

            return d_str

    return TimestampLeafTag
