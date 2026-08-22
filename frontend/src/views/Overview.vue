<template>
  <dashboard v-if="dataset">
    <h2>{{ $t("sections.overview") }}</h2>

    <div
      v-if="filter"
      class="row"
    >
      <div class="col col-12 col-xl-6 filtered">
        <h4>
          {{ $t("overview.filtered.title") }}
          <Tooltip :text="$t('overview.filtered.info')" />
        </h4>
        <div class="result_box">
          <dl
            v-if="data_quality"
            class="metadata_list row"
          >
            <dt class="col-6">
              {{ $t("overview.filtered.original") }}
            </dt>
            <dd class="col-6">
              {{ dataset.parent_name }}
              <span class="dataset_id">(Id {{ dataset.parent_id }})</span>
            </dd>
            <dt class="col-6">
              {{ $t("datasetFilter.releaseDateFrom") }}
            </dt>
            <dd class="col-6">
              {{ filter?.release_date_from }}
            </dd>
            <dt class="col-6">
              {{ $t("datasetFilter.releaseDateTo") }}
            </dt>
            <dd class="col-6">
              {{ filter?.release_date_to }}
            </dd>
            <dt class="col-6">
              {{ $t("datasetFilter.buyerNameRegex") }}
            </dt>
            <dd class="col-6">
              {{ filter?.buyer_regex }}
            </dd>
            <dt class="col-6">
              {{ $t("datasetFilter.procuringEntityNameRegex") }}
            </dt>
            <dd class="col-6">
              {{ filter?.procuring_entity_regex }}
            </dd>
            <dt class="col-6">
              {{ $t("datasetFilter.buyerName") }}
            </dt>
            <dd class="col-6">
              {{ filtered_buyer.join(", ") }}
            </dd>
            <dt class="col-6">
              {{ $t("datasetFilter.procuringEntityName") }}
            </dt>
            <dd class="col-6">
              {{ filtered_procuring_entity.join(", ") }}
            </dd>
          </dl>
        </div>
      </div>
    </div>

    <div class="row">
      <div class="col-12 col-xl-6">
        <h4>
          {{ $t("overview.collection_metadata") }}
          <Tooltip :text="$t('overview.collection_metadata_tooltip')" />
        </h4>
        <div class="result_box collection_metadata col col-12">
          <dl
            v-if="collection"
            class="metadata_list row"
          >
            <dt class="col-4 d-flex align-items-center">
              {{ $t("overview.compiled_releases.value_label") }}
            </dt>
            <dd class="col-8 d-flex align-items-center break_word">
              <span class="ocid_count bold">{{
                formatNumber(compiled_releases?.total_unique_ocids)
              }}</span>
            </dd>
            <dt class="col-4 d-flex align-items-center">
              {{ $t("overview.publisher") }}
            </dt>
            <dd class="col-8 d-flex align-items-center break_word">
              {{ collection.publisher }}
            </dd>
            <dt class="col-4 d-flex align-items-center">
              {{ $t("overview.ocidPrefix") }}
            </dt>
            <dd class="col-8 d-flex align-items-center">
              {{ collection.ocid_prefix }}
            </dd>
            <dt class="col-4 d-flex align-items-center">
              {{ $t("overview.dataLicense") }}
            </dt>
            <dd class="col-8 d-flex align-items-center break_word">
              <a
                v-if="collection.data_license"
                :href="collection.data_license"
                target="_blank"
              >{{
                collection.data_license
              }}</a>
            </dd>
            <dt class="col-4 d-flex align-items-center">
              {{ $t("overview.publicationPolicy") }}
            </dt>
            <dd class="col-8 d-flex align-items-center break_word">
              <a
                v-if="collection.publication_policy"
                :href="collection.publication_policy"
                target="_blank"
              >{{ collection.publication_policy }}</a>
            </dd>
            <dt class="col-4 d-flex align-items-center">
              {{ $t("overview.extensions") }}
            </dt>
            <dd class="col-8">
              <template v-for="(e, i) in extensions" :key="i">
                <a
                  v-if="e.url"
                  :href="e.url"
                  target="_blank"
                >{{ e.name }}</a>
                <a
                  v-else
                  target="_blank"
                >{{ e.name }}</a><template v-if="i + 1 < extensions.length">, </template>
              </template>
            </dd>
            <dt class="col-4 d-flex align-items-center">
              {{ $t("overview.publishedFrom") }}
            </dt>
            <dd class="col-8 d-flex align-items-center">
              {{ collection.published_from }}
            </dd>
            <dt class="col-4 d-flex align-items-center">
              {{ $t("overview.publishedTo") }}
            </dt>
            <dd class="col-8 d-flex align-items-center">
              {{ collection.published_to }}
            </dd>
          </dl>
        </div>
      </div>
      <div class="col-12 col-xl-6">
        <div class="row">
          <div class="col-12 col-md-6 col-xl-12">
            <h4>{{ $t("overview.kingfisher_metadata") }}</h4>
            <div class="result_box collection_metadata kingfisher_metadata">
              <dl
                v-if="kingfisher"
                class="metadata_list row"
              >
                <dt class="col-6">
                  {{ $t("overview.collectionId") }}
                </dt>
                <dd class="col-6">
                  {{ kingfisher.collection_id }}
                </dd>
                <dt class="col-6">
                  {{ $t("overview.kingfisher_processingFrom") }}
                </dt>
                <dd class="col-6">
                  {{ kingfisher.processing_start }}
                </dd>
                <dt class="col-6">
                  {{ $t("overview.kingfisher_processingTo") }}
                </dt>
                <dd class="col-6">
                  {{ kingfisher.processing_end }}
                </dd>
              </dl>
            </div>
          </div>

          <div class="col-12 col-md-6 col-xl-12">
            <h4>{{ $t("overview.dqt_metadata") }}</h4>
            <div class="result_box collection_metadata kingfisher_metadata dqt_metadata">
              <dl
                v-if="data_quality"
                class="metadata_list row"
              >
                <dt class="col-6">
                  {{ $t("overview.processingFrom") }}
                </dt>
                <dd class="col-6">
                  {{ data_quality.processing_start }}
                </dd>
                <dt class="col-6">
                  {{ $t("overview.processingTo") }}
                </dt>
                <dd class="col-6">
                  {{ data_quality.processing_end }}
                </dd>
              </dl>
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
            <template v-for="n in PHASE_NAMES" :key="n">
              <div
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
                  <strong>{{ formatNumber(lifecycle?.[n]) }}</strong>
                </div>
              </div>
              <div
                v-if="n != 'implementation'"
                :key="n + '-arrow'"
                class="col-auto px-0 lifecycle_arrow"
              >
                <FontAwesomeIcon icon="long-arrow-alt-right" />
              </div>
            </template>
          </div>
        </div>
      </div>
    </div>
  </dashboard>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import Tooltip from "@/components/Tooltip.vue";
import { useFormatters } from "@/composables/useFormatters";
import { useDatasetStore } from "@/stores/dataset.js";
import Dashboard from "./layouts/Dashboard.vue";

const PHASE_NAMES = ["planning", "tender", "award", "contract", "implementation"] as const;

const datasetStore = useDatasetStore();
const { formatNumber } = useFormatters();
const { locale } = useI18n();

/** The value itself, if a string, or its text in this language, in English, or in whichever it has. */
function localized(value: unknown) {
  if (typeof value === "string") {
    return value;
  }
  if (value !== null && typeof value === "object") {
    const texts = value as Record<string, unknown>;
    const text = texts[locale.value] ?? texts.en ?? Object.values(texts)[0];
    return typeof text === "string" ? text : "";
  }
  return "";
}

const dataset = computed(() => datasetStore.dataset);

const filter = computed(() => dataset.value?.filter_message);

const collection = computed(() => dataset.value?.meta.collection_metadata);
// An extension's metadata is free-form: its name and URL are either a string or an object of localized strings.
const extensions = computed(() =>
  (collection.value?.extensions ?? []).flatMap((extension) => {
    const e = extension as Record<string, unknown>;
    const name = localized(e.name);
    return name ? [{ name, url: localized(e.documentationUrl) || localized(e.repositoryUrl) }] : [];
  }),
);
const kingfisher = computed(() => dataset.value?.meta.kingfisher_metadata);
const data_quality = computed(() => dataset.value?.meta.data_quality_tool_metadata);
const compiled_releases = computed(() => dataset.value?.meta.compiled_releases);
const lifecycle = computed(() => dataset.value?.meta.tender_lifecycle);

const filtered_procuring_entity = computed(() => filter.value?.procuring_entity ?? []);
const filtered_buyer = computed(() => filter.value?.buyer ?? []);
</script>

<style scoped lang="scss">
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
