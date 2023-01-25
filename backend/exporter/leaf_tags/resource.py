from exporter import graphs
from exporter.decorators import leaf
from exporter.util import box_image


@leaf("resultBoxImage")
def result_box_image(tag, data):
    return box_image(
        tag,
        graphs.resource_result_box,
        f"resultBoxImage_{data['name']}.png",
        data["passedCount"],
        data["failedCount"],
        data["notAvailableCount"],
    )
