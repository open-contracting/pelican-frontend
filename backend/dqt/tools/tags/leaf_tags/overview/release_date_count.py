
import datetime

from dqt.tools.tags.tag import LeafTag

class ReleaseDateCountLeafTag(LeafTag):
    MONTH_YEAR_FORMAT = '%b-%y'

    def __init__(self, gdocs, dataset_id):
        super().__init__(
            self.process_tag,
            gdocs,
            dataset_id
        )

        self.set_param_validation(
            'from',
            lambda v: self._is_month_year_format(v),
            description='The value must be in the following format: <month>-<year> (e.g. Feb-19).'
        )
        self.set_param_validation(
            'to',
            lambda v: self._is_month_year_format(v),
            description='The value must be in the following format: <month>-<year> (e.g. Feb-19).'
        )
        
        self.set_required_data_field('period_pairs')

    def process_tag(self, data):
        if self.get_param('from') is not None:
            from_d = datetime.datetime.strptime(self.get_param('from'), ReleaseDateCountLeafTag.MONTH_YEAR_FORMAT)
        else:
            from_d = datetime.datetime.min

        if self.get_param('to') is not None:
            to_d = datetime.datetime.strptime(self.get_param('to'), ReleaseDateCountLeafTag.MONTH_YEAR_FORMAT)
        else:
            to_d = datetime.datetime.max

        total_count = 0
        for period_str, count in data['period_pairs']:
            period_d = datetime.datetime.strptime(period_str, ReleaseDateCountLeafTag.MONTH_YEAR_FORMAT)
            if from_d <= period_d <= to_d:
                total_count += count

        return str(total_count)
            
    def _is_month_year_format(self, s):
        if not isinstance(s, str):
            return False

        try:
            d = datetime.datetime.strptime(s, ReleaseDateCountLeafTag.MONTH_YEAR_FORMAT)
        except ValueError:
            return False

        return True



