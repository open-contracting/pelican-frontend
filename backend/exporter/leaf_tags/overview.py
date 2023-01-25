from exporter import graphs
from exporter.decorators import argument, leaf
from exporter.util import box_image


@argument("stage", required=True, choices={"planning", "tender", "award", "contract", "implementation"})
@leaf("lifecycleObjectCount")
def lifecycle_object_count(tag, data):
    return str(data["lifecycleObjectCounts"][tag.arguments["stage"]])


@leaf("lifecycleImage")
def lifecycle_image(tag, data):
    return box_image(
        tag,
        graphs.lifecycle_image,
        "LifecycleImage.png",
        data["lifecycleObjectCounts"]["planning"],
        data["lifecycleObjectCounts"]["tender"],
        data["lifecycleObjectCounts"]["award"],
        data["lifecycleObjectCounts"]["contract"],
        data["lifecycleObjectCounts"]["implementation"],
    )
