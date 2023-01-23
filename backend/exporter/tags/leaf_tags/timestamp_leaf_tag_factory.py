import datetime

from exporter.tags.tag import LeafTag
from exporter.util import terms_enumeration

DATETIME_FORMATS = {
    "datetime": "%Y-%m-%d %H:%M:%S",
    "date": "%Y-%m-%d",
    "time": "%H:%M:%S",
}


def generate_timestamp_leaf_tag(key, datetime_format):
    class TimestampLeafTag(LeafTag):
        def __init__(self, gdocs, dataset_id):
            super().__init__(self.process_tag, gdocs, dataset_id)

            self.set_param_validation(
                "mode",
                lambda v: v in DATETIME_FORMATS,
                description="The value must be one of the following: %s." % terms_enumeration(DATETIME_FORMATS),
            )

            self.set_required_data_field(key)

        def process_tag(self, data):
            d = datetime.datetime.strptime(data[key], datetime_format)
            mode = self.get_param("mode", "datetime")
            return d.strftime(DATETIME_FORMATS[mode])

    return TimestampLeafTag
