<template>
  <dashboard v-if="dataset">
    <h2>{{ $t("sections.overview") }}</h2>

    <div
      v-if="dataset.filter_message"
      class="row"
    >
      <div class="col col-12 col-xl-6 filtered">
        <h4>
          {{ $t("overview.filtered.title") }}
          <Tooltip :text="$t('overview.filtered.info')" />
        </h4>
        <div class="result_box">
          <div
            v-if="data_quality"
            class="table_hl"
          >
            <div class="tr row">
              <div class="td col col-6">
                {{ $t("overview.filtered.original") }}
              </div>
              <div class="td col col-6">
                {{ dataset.parent_name }}
                <span class="dataset_id">(Id {{ dataset.parent_id }})</span>
              </div>
            </div>
            <div class="tr row">
              <div class="td col col-6">
                {{ $t("datasetFilter.releaseDateFrom") }}
              </div>
              <div class="td col col-6">
                {{ dataset.filter_message.release_date_from }}
              </div>
            </div>
            <div class="tr row">
              <div class="td col col-6">
                {{ $t("datasetFilter.releaseDateTo") }}
              </div>
              <div class="td col col-6">
                {{ dataset.filter_message.release_date_to }}
              </div>
            </div>
            <div class="tr row">
              <div class="td col col-6">
                {{ $t("datasetFilter.buyerNameRegex") }}
              </div>
              <div class="td col col-6">
                {{ dataset.filter_message.buyer_regex }}
              </div>
            </div>
            <div class="tr row">
              <div class="td col col-6">
                {{ $t("datasetFilter.procuringEntityNameRegex") }}
              </div>
              <div class="td col col-6">
                {{ dataset.filter_message.procuring_entity_regex }}
              </div>
            </div>
            <div class="tr row">
              <div class="td col col-6">
                {{ $t("datasetFilter.buyerName") }}
              </div>
              <div class="td col col-6">
                {{ filtered_buyer.join(", ") }}
              </div>
            </div>
            <div class="tr row">
              <div class="td col col-6">
                {{ $t("datasetFilter.procuringEntityName") }}
              </div>
              <div class="td col col-6">
                {{ filtered_procuring_entity.join(", ") }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!--"release_date_from": '2019-12-02',
#         "release_date_to": '2020-02-02',
#         "buyer": ["ministry_of_finance", "state"],
#         "buyer_regex": "Development$",
#         "procuring_entity": ["a", "b"],
        #         "procuring_entity_regex": "(a|b)casdf+"-->

    <div class="row">
      <div class="col-12 col-xl-6">
        <h4>{{ $t("overview.collection_metadata") }}</h4>
        <div class="result_box collection_metadata col col-12">
          <div
            v-if="collection"
            class="table_hl"
          >
            <div class="tr row">
              <div class="td col col-4 d-flex align-items-center">
                {{ $t("overview.compiled_releases.value_label") }}
              </div>
              <div class="td col col-8 d-flex align-items-center break_word">
                <span class="ocid_count bold">{{
                  compiled_releases.total_unique_ocids | formatNumber
                }}</span>
              </div>
            </div>
            <div class="tr row">
              <div class="td col col-4 d-flex align-items-center">
                {{ $t("overview.publisher") }}
              </div>
              <div class="td col col-8 d-flex align-items-center break_word">
                {{ collection.publisher }}
              </div>
            </div>
            <div class="tr row">
              <div class="td col col-4 d-flex align-items-center">
                OCID Prefix
              </div>
              <div class="td col col-8 d-flex align-items-center">
                {{ collection.ocid_prefix }}
              </div>
            </div>
            <div class="tr row">
              <div class="td col col-4 d-flex align-items-center">
                {{ $t("overview.datalicense") }}
              </div>
              <div class="td col col-8 d-flex align-items-center break_word">
                <a
                  v-if="collection.data_license"
                  :href="collection.data_license"
                  target="_blank"
                >{{
                  collection.data_license
                }}</a>
              </div>
            </div>
            <div class="tr row">
              <div class="td col col-4 d-flex align-items-center">
                {{ $t("overview.publicationPolicy") }}
              </div>
              <div class="td col col-8 d-flex align-items-center break_word">
                <a
                  v-if="collection.publication_policy"
                  :href="collection.publication_policy"
                  target="_blank"
                >{{ collection.publication_policy }}</a>
              </div>
            </div>
            <div class="tr row">
              <div class="td col col-4 d-flex align-items-center">
                {{ $t("overview.extensions") }}
              </div>
              <div
                v-if="collection.extensions"
                class="td col col-8"
              >
                <template v-for="(e, i) in collection.extensions">
                  <span
                    v-if="e.hasOwnProperty('name')"
                    :key="i"
                  >
                    <a
                      v-if="
                        e.hasOwnProperty('documentationUrl') &&
                          (e.documentationUrl.hasOwnProperty('en')
                            ? e.documentationUrl['en'] != ''
                            : e.documentationUrl != '')
                      "
                      :key="i"
                      :href="
                        e.documentationUrl.hasOwnProperty('en')
                          ? e.documentationUrl['en']
                          : e.documentationUrl
                      "
                      target="_blank"
                    >{{ e.name.hasOwnProperty("en") ? e.name["en"] : e.name }}</a>
                    <a
                      v-else-if="e.hasOwnProperty('repositoryUrl')"
                      :key="i"
                      :href="e.repositoryUrl"
                      target="_blank"
                    >{{ e.name.hasOwnProperty("en") ? e.name["en"] : e.name }}</a>
                    <a
                      v-else
                      :key="i"
                      target="_blank"
                    >{{
                      e.name.hasOwnProperty("en") ? e.name["en"] : e.name
                    }}</a>
                    <template v-if="i + 1 < collection.extensions.length">, </template>
                  </span>
                </template>
              </div>
            </div>
            <div class="tr row">
              <div class="td col col-4 d-flex align-items-center">
                {{ $t("overview.publishedFrom") }}
              </div>
              <div class="td col col-8 d-flex align-items-center">
                {{ collection.published_from }}
              </div>
            </div>
            <div class="tr row">
              <div class="td col col-4 d-flex align-items-center">
                {{ $t("overview.publishedTo") }}
              </div>
              <div class="td col col-8 d-flex align-items-center">
                {{ collection.published_to }}
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-12 col-xl-6">
        <div class="row">
          <div class="col-12 col-md-6 col-xl-12">
            <h4>{{ $t("overview.kingfisher_metadata") }}</h4>
            <div class="result_box collection_metadata kingfisher_metadata">
              <div
                v-if="kingfisher"
                class="table_hl"
              >
                <div class="tr row">
                  <div class="td col col-6">
                    {{ $t("overview.collectionId") }}
                  </div>
                  <div class="td col col-6">
                    {{ kingfisher.collection_id }}
                  </div>
                </div>
                <div class="tr row">
                  <div class="td col col-6">
                    {{ $t("overview.kingfisher_processingFrom") }}
                  </div>
                  <div class="td col col-6">
                    {{ kingfisher.processing_start }}
                  </div>
                </div>
                <div class="tr row">
                  <div class="td col col-6">
                    {{ $t("overview.kingfisher_processingTo") }}
                  </div>
                  <div class="td col col-6">
                    {{ kingfisher.processing_end }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="col-12 col-md-6 col-xl-12">
            <h4>{{ $t("overview.dqt_metadata") }}</h4>
            <div class="result_box collection_metadata kingfisher_metadata dqt_metadata">
              <div
                v-if="data_quality"
                class="table_hl"
              >
                <div class="tr row">
                  <div class="td col col-6">
                    {{ $t("overview.processingFrom") }}
                  </div>
                  <div class="td col col-6">
                    {{ data_quality.processing_start }}
                  </div>
                </div>
                <div class="tr row">
                  <div class="td col col-6">
                    {{ $t("overview.processingTo") }}
                  </div>
                  <div class="td col col-6">
                    {{ data_quality.processing_end }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <div class="col col-12 lifecycle">
        <h4>
          {{ $t("overview.lifecycle.title") }}
          <Tooltip :text="$t('overview.lifecycle.info')" />
        </h4>
        <div class="result_box">
          <div class="row">
            <template v-for="n in ['planning', 'tender', 'award', 'contract', 'implementation']">
              <div
                :key="n"
                class="col col-sm-2 col-md text-center lifecycle_phase"
              >
                <div class="lifecycle_label">
                  {{ $t("overview.lifecycle." + n) }}
                </div>
                <div class="icon">
                  <img
                    class="lifecycle_icon"
                    :src="'/img/icons/' + n + '_icon.png'"
                  >
                </div>
                <div class="lifecycle_value">
                  <strong>{{ lifecycle[n] | formatNumber }}</strong>
                </div>
              </div>
              <div
                v-if="n != 'implementation'"
                :key="n + '-arrow'"
                class="lifecycle_arrow"
              >
                <font-awesome-icon icon="long-arrow-alt-right" />
              </div>
            </template>
          </div>
        </div>
      </div>
    </div>
  </dashboard>
</template>

<script>
import Dashboard from "@/views/layouts/Dashboard.vue";
import Tooltip from "@/components/Tooltip.vue";

export default {
    name: "Overview",
    components: { Dashboard, Tooltip },
    computed: {
        dataset: function () {
            return this.$store.getters.dataset;
        },
        collection: function () {
            return this.getMetaData("collection_metadata");
        },
        kingfisher: function () {
            return this.getMetaData("kingfisher_metadata");
        },
        data_quality: function () {
            return this.getMetaData("data_quality_tool_metadata");
        },
        compiled_releases: function () {
            return this.getMetaData("compiled_releases");
        },
        lifecycle: function () {
            return this.getMetaData("tender_lifecycle");
        },
        filtered_procuring_entity: function () {
            if (this.dataset.filter_message.procuring_entity) {
                return this.dataset.filter_message.procuring_entity;
            }

            return [];
        },
        filtered_buyer: function () {
            if (this.dataset.filter_message.buyer) {
                return this.dataset.filter_message.buyer;
            }

            return [];
        }
    },
    methods: {
        getMetaData: function (type) {
            return this.dataset && this.dataset.meta ? this.dataset.meta[type] : null;
        },
        formatNumber(number) {
            return this.$options.filters.formatNumber(number);
        },
        extensionPreview(extensionName) {
            this.$router.push({
                name: "extensionPreview",
                params: {
                    extensionName: extensionName,
                    datasetId: this.$store.getters.datasetId
                }
            });
        }
    }
};
</script>

<style lang="scss">
@import "src/scss/main";

.ocid_count {
    font-size: 24px;
}

.tr:first-of-type .td {
    border-top: none;
}

.lifecycle_phase {
    margin-bottom: 20px;
}

.lifecycle_icon {
    width: 35px;
    margin-bottom: 10px;
    margin-top: 10px;
}

.lifecycle_arrow {
    padding-top: 40px;
}

.lifecycle_value {
    font-size: 20px;
    font-weight: 500;
    line-height: 24px;
    text-align: center;
}
</style>
