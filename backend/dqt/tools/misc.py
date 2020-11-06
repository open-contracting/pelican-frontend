
import datetime


def terms_enumeration(it):
    return ', '.join(
        ('\'%s\'' % el)
        for el in it
    )


# parses %b-%y and %b-%-y format
# respective examples are Nov-8, Nov-08
MONTH_YEAR_FORMAT = '%b-%y'
def parse_month_year(s):
    if not isinstance(s, str):
        return None

    if not 5 <= len(s) <= 6:
        return None

    if len(s) == 5:
        s = s[:4] + '0' + s[4]

    try:
        return datetime.datetime.strptime(s, MONTH_YEAR_FORMAT)
    except ValueError:
        return None
