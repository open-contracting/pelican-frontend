from exporter import graphs
from exporter.decorators import argument, leaf
from exporter.util import MODES, box_image, sample_and_format

COUNT_RANGES = {"1", "2-20", "21-50", "51-100", "100+"}
PERCENTAGE_RANGES = {"0-1", "1-5", "5-20", "20-50", "50-100"}
RANKS = {"1", "2", "3", "4", "5"}


@leaf("result")
def result(tag, data):
    if data["result"] is True:
        return "Passed"
    if data["result"] is False:
        return "Failed"
    if data["result"] is None:
        return "Undefined"
    raise ValueError(f"Unknown result: '{data['result']}'")


@leaf("value")
def value(tag, data):
    if data["value"] is None:
        return "Undefined"
    return str(data["value"])


@argument("countRange", choices=COUNT_RANGES)
@leaf("ocidCount")
def ocid_count(tag, data):
    if "countRange" in tag.arguments:
        return str(data["ocidCounts"][tag.arguments["countRange"]])
    return str(sum(data["ocidCounts"].values()))


@argument("countRange", choices=COUNT_RANGES)
@leaf("buyerCount")
def buyer_count(tag, data):
    if "countRange" in tag.arguments:
        return str(data["buyerCounts"][tag.arguments["countRange"]])
    return str(sum(data["buyerCounts"].values()))


@argument("percentageRange", choices=PERCENTAGE_RANGES)
@leaf("count")
def bar_count(tag, data):
    if "percentageRange" in tag.arguments:
        return str(data["counts"][tag.arguments["percentageRange"]])
    return str(sum(data["counts"].values()))


@argument("percentageRange", choices=PERCENTAGE_RANGES)
@leaf("sum")
def bar_sum(tag, data):
    if "percentageRange" in tag.arguments:
        return str(data["sums"][tag.arguments["percentageRange"]])
    return str(sum(data["sums"].values()))


@argument("percentageRange", choices=PERCENTAGE_RANGES)
@argument("decimals", type=int, default=0)
@leaf("share")
def bar_share(tag, data):
    if "percentageRange" in tag.arguments:
        share = 100 * data["shares"][tag.arguments["percentageRange"]]
    else:
        share = 100.0
    return f"%.{tag.arguments['decimals']}f" % share


@argument("percentageRange", choices=PERCENTAGE_RANGES)
@argument("mode", choices=MODES, default="oneLine")
@argument("max", type=int, nonzero=True)
@leaf("examples")
def bar_examples(tag, data):
    if "percentageRange" in tag.arguments:
        examples = data["examples"][tag.arguments["percentageRange"]]
    else:
        examples = [example for examples in data["examples"].values() for example in examples]
    return sample_and_format(examples, tag.arguments)


@argument("value")
@leaf("count")
def donut_count(tag, data):
    if "value" not in tag.arguments:
        return str(sum(data["counts"].values()))
    if tag.arguments["value"] in data["counts"]:
        return str(data["counts"][tag.arguments["value"]])
    return "0"


@argument("value")
@argument("decimals", type=int, default=0)
@leaf("share")
def donut_share(tag, data):
    if "value" not in tag.arguments:
        share = 100.0
    elif tag.arguments["value"] in data["shares"]:
        share = 100 * data["shares"][tag.arguments["value"]]
    else:
        share = 0.0
    return f"%.{tag.arguments['decimals']}f" % share


@argument("value")
@argument("mode", choices=MODES, default="oneLine")
@argument("max", type=int, nonzero=True)
@leaf("examples")
def donut_examples(tag, data):
    if "value" not in tag.arguments:
        examples = [example for examples in data["examples"].values() for example in examples]
    elif tag.arguments["value"] in data["examples"]:
        examples = data["examples"][tag.arguments["value"]]
    else:
        examples = []
    return sample_and_format(examples, tag.arguments)


@argument("rank", required=True, choices=RANKS)
@leaf("amount")
def top3_amount(tag, data):
    return str(data["amounts"][tag.arguments["rank"]])


@argument("rank", choices=RANKS)
@leaf("count")
def top3_count(tag, data):
    if "rank" in tag.arguments:
        return str(data["counts"][tag.arguments["rank"]])
    return str(sum(data["counts"].values()))


@argument("rank", choices=RANKS)
@argument("decimals", type=int, default=0)
@leaf("share")
def top3_share(tag, data):
    if "rank" in tag.arguments:
        share = 100 * data["shares"][tag.arguments["rank"]]
    else:
        share = 100.0
    return f"%.{tag.arguments['decimals']}f" % share


@argument("rank", choices=RANKS)
@argument("mode", choices=MODES, default="oneLine")
@argument("max", type=int, nonzero=True)
@leaf("examples")
def top3_examples(tag, data):
    if "rank" in tag.arguments:
        examples = data["examples"][tag.arguments["rank"]]
    else:
        examples = [example for examples in data["examples"].values() for example in examples]
    return sample_and_format(examples, tag.arguments)


@argument("type", choices={"bar"}, default="bar")
@leaf("resultBoxImage")
def counts_result_box_image(tag, data):
    return box_image(
        tag,
        graphs.bar_result_box,
        f"resultBoxImage_{data['name']}.png",
        data["counts_pairs"],
    )


@leaf("resultBoxImage")
def passed_result_box_image(tag, data):
    return box_image(
        tag,
        graphs.passed_result_box,
        f"resultBoxImage_{tag.arguments.get('level')}_{data['name']}.png",
        data["passedCount"],
        data["failedCount"],
    )


@leaf("resultBoxImage")
def table_result_box_image(tag, data):
    return box_image(
        tag,
        graphs.table_result_box,
        f"resultBoxImage_{data['name']}.png",
        data["counts_pairs"],
        data["total_count"],
    )
