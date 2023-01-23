import datetime

COUNT_RANGES = {"1", "2-20", "21-50", "51-100", "100+"}
LEVELS = ("coverage", "coverageSet", "coverageEmpty", "quality")
MODES = ("oneLine", "multipleLines")
PERCENTAGE_RANGES = {"0-1", "1-5", "5-20", "20-50", "50-100"}
RANKS = {"1", "2", "3", "4", "5"}

# parses %b-%y and %b-%-y format
# respective examples are Nov-8, Nov-08
MONTH_YEAR_FORMAT = "%b-%y"


def terms_enumeration(it):
    return ", ".join(f"'{el}'" for el in it)


def parse_month_year(s):
    if not isinstance(s, str):
        return None

    if not 5 <= len(s) <= 6:
        return None

    if len(s) == 5:
        s = s[:4] + "0" + s[4]

    try:
        return datetime.datetime.strptime(s, MONTH_YEAR_FORMAT)
    except ValueError:
        return None
