from drf_spectacular.extensions import OpenApiSerializerExtension
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api.models import DataItem, Dataset


class DataItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataItem
        fields = ["id", "data"]


class FilterDatasetSerializer(serializers.Serializer):
    release_date_from = serializers.CharField(required=False, help_text="The minimum release date (YYYY-MM-DD)")
    release_date_to = serializers.CharField(required=False, help_text="The maximum release date (YYYY-MM-DD)")
    buyer = serializers.ListField(required=False, child=serializers.CharField(), help_text="Names of buyers")
    buyer_regex = serializers.CharField(required=False, help_text="A SQL ILIKE pattern for the buyer's name")
    procuring_entity = serializers.ListField(
        required=False, child=serializers.CharField(), help_text="Names of procuring entities"
    )
    procuring_entity_regex = serializers.CharField(
        required=False, help_text="A SQL ILIKE pattern for the procuring entity's name"
    )


class CollectionMetadataSerializer(serializers.Serializer):
    publisher = serializers.CharField(allow_null=True, help_text="The publisher's name")
    ocid_prefix = serializers.CharField(allow_null=True, help_text="The OCID prefix")
    published_from = serializers.CharField(allow_null=True, help_text="The earliest release date")
    published_to = serializers.CharField(allow_null=True, help_text="The latest release date")
    data_license = serializers.CharField(allow_null=True, help_text="The URL of the data license")
    publication_policy = serializers.CharField(allow_null=True, help_text="The URL of the publication policy")
    # An OCDS extension's own metadata, whose properties vary by extension.
    extensions = serializers.ListField(child=serializers.JSONField(), help_text="The declared extensions")


class PelicanMetadataSerializer(serializers.Serializer):
    processing_start = serializers.CharField(help_text="When Pelican started processing the dataset")
    processing_end = serializers.CharField(help_text="When Pelican finished processing the dataset")


# Empty if the collection has no rows in Kingfisher Process.
class KingfisherMetadataSerializer(serializers.Serializer):
    collection_id = serializers.IntegerField(
        required=False, help_text="The compiled collection ID in Kingfisher Process"
    )
    processing_start = serializers.CharField(
        required=False, help_text="When Kingfisher Process started storing the original collection"
    )
    processing_end = serializers.CharField(
        required=False, help_text="When Kingfisher Process finished storing the compiled collection"
    )


class CompiledReleasesSerializer(serializers.Serializer):
    total_unique_ocids = serializers.IntegerField(help_text="The number of distinct OCIDs")


class TenderLifecycleSerializer(serializers.Serializer):
    planning = serializers.IntegerField()
    tender = serializers.IntegerField()
    award = serializers.IntegerField()
    contract = serializers.IntegerField()
    implementation = serializers.IntegerField()


class DatasetMetaSerializer(serializers.Serializer):
    collection_metadata = CollectionMetadataSerializer()
    kingfisher_metadata = KingfisherMetadataSerializer()
    # Pelican writes its metadata when it finishes, so an in-progress dataset has none.
    data_quality_tool_metadata = PelicanMetadataSerializer(required=False)
    compiled_releases = CompiledReleasesSerializer()
    tender_lifecycle = TenderLifecycleSerializer(help_text="The number of objects in each stage")


@extend_schema_field(DatasetMetaSerializer)
class DatasetMetaField(serializers.JSONField):
    """Document the column's structure without validating it, so that a new key is not dropped."""


@extend_schema_field(FilterDatasetSerializer)
class FilterMessageField(serializers.JSONField):
    """Document the column's structure without validating it, so that a new key is not dropped."""


class DatasetSerializer(serializers.ModelSerializer):
    meta = DatasetMetaField()
    phase = serializers.CharField()
    state = serializers.CharField()
    # Null, unless the dataset is the result of a filter.
    parent_id = serializers.IntegerField(allow_null=True, help_text="The ID of the dataset that was filtered")
    parent_name = serializers.CharField(allow_null=True, help_text="The name of the dataset that was filtered")
    filter_message = FilterMessageField(allow_null=True, help_text="The filter that created the dataset")

    class Meta:
        model = Dataset
        fields = [
            "id",
            "name",
            "meta",
            "ancestor_id",
            "created",
            "modified",
            "phase",
            "state",
            "parent_id",
            "parent_name",
            "filter_message",
        ]


class CreateDatasetSerializer(serializers.Serializer):
    name = serializers.CharField(
        help_text="The name to assign to the dataset",
        validators=[UniqueValidator(queryset=Dataset.objects.all())],
    )
    collection_id = serializers.IntegerField(help_text="The compiled collection ID in Kingfisher Process")
    ancestor_id = serializers.IntegerField(
        required=False, help_text="The ID of the previous report in Pelican, for time-based checks"
    )
    max_items = serializers.IntegerField(
        required=False, help_text="The number of compiled releases to import from Kingfisher Process"
    )


class CountDatasetFilterItemsSerializer(serializers.Serializer):
    dataset_id_original = serializers.IntegerField(help_text="The ID of the dataset to filter")
    filter_message = FilterDatasetSerializer(help_text="The filter to apply")


class DistinctValueSerializer(serializers.Serializer):
    value = serializers.CharField(help_text="The field's value")
    count = serializers.IntegerField(help_text="The number of data items with this value")


class SettingsSerializer(serializers.Serializer):
    user = serializers.CharField(help_text="The service account that the template and folder must be shared with")
    template = serializers.DictField(
        child=serializers.CharField(), help_text="The ID of the default Google Docs template, by language"
    )
    folder = serializers.CharField(help_text="The ID of the default Google Drive folder in which to create reports")


class ExampleMetaSerializer(serializers.Serializer):
    ocid = serializers.CharField(help_text="The compiled release's OCID")
    item_id = serializers.IntegerField(help_text="The data item's ID")


class FieldLevelExampleResultSerializer(serializers.Serializer):
    name = serializers.CharField(help_text="The check's name")
    result = serializers.BooleanField(help_text="Whether the check passed")
    reason = serializers.CharField(allow_null=True, help_text="The reason the check failed")
    value = serializers.JSONField(allow_null=True, help_text="The field's value, if the check failed")
    version = serializers.FloatField(help_text="The check's version")


class FieldLevelExampleSerializer(serializers.Serializer):
    meta = ExampleMetaSerializer()
    path = serializers.CharField(help_text="The field's path")
    result = FieldLevelExampleResultSerializer()


class ResourceLevelExampleResultSerializer(serializers.Serializer):
    result = serializers.BooleanField(allow_null=True, help_text="Whether the check passed")
    meta = serializers.JSONField(
        allow_null=True, help_text="Any additional data to help interpret the result. Its properties vary by check."
    )
    pass_count = serializers.IntegerField(allow_null=True, help_text="The number of times the check passed")
    application_count = serializers.IntegerField(
        allow_null=True, help_text="The number of times the check was applied"
    )
    version = serializers.FloatField(help_text="The check's version")


class ResourceLevelExampleSerializer(serializers.Serializer):
    meta = ExampleMetaSerializer()
    result = ResourceLevelExampleResultSerializer()


class ReportSerializer(serializers.Serializer):
    """A report, as an object keyed by check name. Subclasses set ``check_serializer``."""

    check_serializer = None


class ReportSerializerExtension(OpenApiSerializerExtension):
    target_class = ReportSerializer
    match_subclasses = True

    def map_serializer(self, auto_schema, direction):
        component = auto_schema.resolve_serializer(self.target.check_serializer(), direction)
        return {"type": "object", "additionalProperties": component.ref}


# The counts are per occurrence of the field, which can exceed the number of compiled releases.
# Only field_level/{name}/ returns the examples. A report omits them.
class FieldLevelCountsSerializer(serializers.Serializer):
    total_count = serializers.IntegerField(help_text="The number of times the check was applied")
    passed_count = serializers.IntegerField(help_text="The number of times the check passed")
    failed_count = serializers.IntegerField(help_text="The number of times the check failed")
    passed_examples = FieldLevelExampleSerializer(many=True, required=False)
    failed_examples = FieldLevelExampleSerializer(many=True, required=False)


class FieldLevelGroupSerializer(FieldLevelCountsSerializer):
    checks = serializers.DictField(child=FieldLevelCountsSerializer(), help_text="The checks, by name")


class FieldLevelCheckSerializer(serializers.Serializer):
    coverage = FieldLevelGroupSerializer()
    quality = FieldLevelGroupSerializer()
    examples_filled = serializers.BooleanField(help_text="Whether the examples are filled in")
    processing_order = serializers.IntegerField(help_text="The order in which to display the field")


class FieldLevelReportSerializer(ReportSerializer):
    check_serializer = FieldLevelCheckSerializer


class FieldLevelCountsDetailSerializer(FieldLevelCountsSerializer):
    passed_examples = FieldLevelExampleSerializer(many=True)
    failed_examples = FieldLevelExampleSerializer(many=True)


class FieldLevelGroupDetailSerializer(FieldLevelCountsDetailSerializer):
    checks = serializers.DictField(child=FieldLevelCountsDetailSerializer(), help_text="The checks, by name")


class FieldLevelCheckDetailSerializer(FieldLevelCheckSerializer):
    coverage = FieldLevelGroupDetailSerializer()
    quality = FieldLevelGroupDetailSerializer()
    time = serializers.FloatField(help_text="The duration of the request, in seconds")


# Only compiled_release_level/{name}/ returns the examples. In a report, they are empty.
class ResourceLevelCheckSerializer(serializers.Serializer):
    name = serializers.CharField(help_text="The check's name")
    total_count = serializers.IntegerField(help_text="The number of compiled releases to which the check was applied")
    passed_count = serializers.IntegerField(help_text="The number of compiled releases that passed")
    failed_count = serializers.IntegerField(help_text="The number of compiled releases that failed")
    undefined_count = serializers.IntegerField(
        help_text="The number of compiled releases for which the check was inapplicable"
    )
    individual_application_count = serializers.IntegerField(help_text="The number of times the check was applied")
    individual_passed_count = serializers.IntegerField(help_text="The number of times the check passed")
    individual_failed_count = serializers.IntegerField(help_text="The number of times the check failed")
    examples_filled = serializers.BooleanField(help_text="Whether the examples are filled in")
    passed_examples = ResourceLevelExampleSerializer(many=True)
    failed_examples = ResourceLevelExampleSerializer(many=True)
    undefined_examples = ResourceLevelExampleSerializer(many=True)


class ResourceLevelReportSerializer(ReportSerializer):
    check_serializer = ResourceLevelCheckSerializer


class ResourceLevelCheckDetailSerializer(ResourceLevelCheckSerializer):
    time = serializers.FloatField(help_text="The duration of the request, in seconds")


class DatasetLevelCheckSerializer(serializers.Serializer):
    result = serializers.BooleanField(allow_null=True, help_text="Whether the check passed, or null if not applicable")
    value = serializers.IntegerField(allow_null=True)
    meta = serializers.JSONField(
        help_text="Any additional data to help interpret the result. Its properties vary by check."
    )


class DatasetLevelReportSerializer(ReportSerializer):
    check_serializer = DatasetLevelCheckSerializer


class TimeVarianceExampleSerializer(serializers.Serializer):
    ocid = serializers.CharField(help_text="The pair's OCID")
    item_id = serializers.IntegerField(help_text="The data item's ID in the ancestor dataset")
    new_item_ocid = serializers.CharField(help_text="The same value as ocid, since a pair is matched on it")
    new_item_id = serializers.IntegerField(help_text="The data item's ID in this dataset")


class TimeVarianceMetaSerializer(serializers.Serializer):
    total_count = serializers.IntegerField(
        help_text="The number of the ancestor dataset's compiled releases to which the check applies"
    )
    coverage_count = serializers.IntegerField(
        help_text="The number of the ancestor dataset's applicable compiled releases that are paired"
    )
    ok_count = serializers.IntegerField(help_text="The number of pairs that passed")
    failed_count = serializers.IntegerField(help_text="The number of pairs that failed")
    examples = TimeVarianceExampleSerializer(many=True, help_text="A sample of up to 50 pairs that failed")
    version = serializers.FloatField(help_text="The check's version")


class TimeVarianceLevelCheckSerializer(serializers.Serializer):
    """A pair is a compiled release in the ancestor dataset and the one with the same OCID in this dataset."""

    coverage_value = serializers.IntegerField(
        allow_null=True,
        help_text="The percentage of the ancestor dataset's applicable compiled releases that are paired, "
        "or null if the check applied to none",
    )
    coverage_result = serializers.BooleanField(allow_null=True, help_text="Whether coverage_value exceeds 95")
    check_value = serializers.IntegerField(
        allow_null=True, help_text="The percentage of pairs that passed, or null if none were found"
    )
    check_result = serializers.BooleanField(allow_null=True, help_text="Whether check_value exceeds 95")
    meta = TimeVarianceMetaSerializer()


class TimeVarianceLevelReportSerializer(ReportSerializer):
    check_serializer = TimeVarianceLevelCheckSerializer
