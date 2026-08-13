<template>
  <span class="just_holder">
    <Loader v-if="isSubmitting && submitResult == null" />
    <BAlert
      v-if="isSubmitting && submitResult != null"
      variant="success"
      :model-value="true"
    >{{
      $t("datasetFilter.statusOk")
    }}</BAlert>
    <form
      v-if="!isSubmitting"
      class="modal_box align-items-center"
    >
      <div class="row mb-3">
        <label class="col-4 col-form-label">{{ $t("datasetFilter.releaseDateFromTo") }}</label>
        <div class="col-8 modal_input">
          <div class="row">
            <div class="col">
              <input
                v-model="releaseDateFrom"
                type="date"
                :min="firstDate"
                :max="lastDate"
                class="form-control"
              >
            </div>
            <div class="col">
              <input
                v-model="releaseDateTo"
                type="date"
                :min="firstDate"
                :max="lastDate"
                class="form-control"
              >
            </div>
          </div>
        </div>
      </div>
      <div class="row mb-3 section_row">
        <label class="col-4 col-form-label">{{ $t("datasetFilter.buyerName") }}</label>
        <div class="col-8">
          <DatasetValuesMultiselect
            :update-selected="updateBuyerName"
            :dataset-id="dataset?.id"
            json-path="buyer.name"
          />
        </div>
      </div>
      <div class="row mb-3">
        <label class="col-4 col-form-label">{{ $t("datasetFilter.procuringEntityName") }}</label>
        <div class="col-8">
          <DatasetValuesMultiselect
            :update-selected="updateProcuringEntityName"
            :dataset-id="dataset?.id"
            json-path="tender.procuringEntity.name"
          />
        </div>
      </div>
      <div class="row mb-3 section_row">
        <label class="col-4 col-form-label">{{ $t("datasetFilter.buyerNameRegex") }}</label>
        <div class="col-8">
          <input
            v-model="buyerNameRegex"
            class="regex_input"
          >
          <small class="form-text text-body-secondary">{{ $t("datasetFilter.buyerNameRegexTooltip") }}</small>
        </div>
      </div>
      <div class="row mb-3 procuring_row">
        <label class="col-4 col-form-label">{{ $t("datasetFilter.procuringEntityNameRegex") }}</label>
        <div class="col-8">
          <input
            v-model="procuringEntityNameRegex"
            class="regex_input"
          >
          <small class="form-text text-body-secondary">{{
            $t("datasetFilter.procuringEntityNameRegexTooltip")
          }}</small>
        </div>
      </div>
      <div class="text-center">
        <button
          type="button"
          class="btn btn-primary submit_button"
          :disabled="items == 0 || (dataset != null && items == dataset.meta.compiled_releases?.total_unique_ocids) || gettingCountsToken != null"
          @click="createDatasetFilter"
        >
          {{ $t("datasetFilter.submit") }}
          <span v-if="gettingCountsToken == null">
            <span
              v-if="items != null && items > 0 && dataset != null && items != dataset.meta.compiled_releases?.total_unique_ocids"
            >({{ formatNumber(items) }} from {{ formatNumber(dataset.meta.compiled_releases?.total_unique_ocids) }}
              {{ $t("datasetFilter.items") }})</span>
            <span
              v-if="dataset != null && items == dataset.meta.compiled_releases?.total_unique_ocids"
            >({{ $t("datasetFilter.itemsAll") }})</span>
          </span>
          <BSpinner
            v-if="gettingCountsToken != null"
            style="width: 1.2rem; height: 1.2rem"
          />
        </button>
      </div>
    </form>
  </span>
</template>

<script setup>
import axios from "axios";
import { BAlert, BSpinner } from "bootstrap-vue-next";
import { computed, onMounted, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import { useFormatters } from "@/composables/useFormatters";
import { CONFIG } from "@/config.js";
import DatasetValuesMultiselect from "./DatasetValuesMultiselect.vue";
import Loader from "./Loader.vue";

const props = defineProps(["dataset"]);
const emit = defineEmits(["close"]);

const router = useRouter();
const { t } = useI18n();
const { formatNumber } = useFormatters();

const isSubmitting = ref(false);
const submitResult = ref(null);
const items = ref(null);
const releaseDateFrom = ref(null);
const releaseDateTo = ref(null);
const buyerName = ref([]);
const procuringEntityName = ref([]);
const buyerNameRegex = ref("");
const procuringEntityNameRegex = ref("");

let gettingCountsToken = null;
let filteredItemsTimeout = null;
const filteredItemsTimeoutLimit = 400;

const firstDate = computed(() => {
    const publishedFrom = props.dataset.meta.collection_metadata.published_from;
    if (publishedFrom) {
        return publishedFrom.substring(0, 10);
    }
    return "1970-01-01";
});

const lastDate = computed(() => {
    const publishedTo = props.dataset.meta.collection_metadata.published_to;
    if (publishedTo) {
        return publishedTo.substring(0, 10);
    }
    return new Date().toISOString().split("T")[0];
});

function datasetFilterMessage() {
    if (props.dataset == null) {
        return null;
    }

    const data = {};

    if (releaseDateFrom.value > firstDate.value) {
        data.release_date_from = releaseDateFrom.value;
    }
    if (releaseDateTo.value < lastDate.value) {
        data.release_date_to = releaseDateTo.value;
    }
    if (buyerName.value.length > 0) {
        data.buyer = buyerName.value;
    }
    if (buyerNameRegex.value.trim() !== "") {
        data.buyer_regex = buyerNameRegex.value.trim();
    }
    if (procuringEntityName.value.length > 0) {
        data.procuring_entity = procuringEntityName.value;
    }
    if (procuringEntityNameRegex.value.trim() !== "") {
        data.procuring_entity_regex = procuringEntityNameRegex.value.trim();
    }

    return data;
}

function datasetFilterItems() {
    if (props.dataset == null) {
        return;
    }

    // https://axios-http.com/docs/cancellation
    if (gettingCountsToken != null) {
        gettingCountsToken.cancel();
    }

    gettingCountsToken = axios.CancelToken.source();

    axios
        .post(
            `${CONFIG.apiBaseUrl}${CONFIG.apiEndpoints.datasetFilterItems}`,
            {
                dataset_id_original: Number.parseInt(props.dataset.id, 10),
                filter_message: datasetFilterMessage(),
            },
            {
                cancelToken: gettingCountsToken.token,
            },
        )
        .then((response) => {
            if (response.status === 200) {
                items.value = response.data.items;
            } else {
                items.value = null;
            }

            gettingCountsToken = null;
        })
        .catch((error) => {
            if (!axios.isCancel(error)) {
                throw new Error(error);
            }
        });
}

function createDatasetFilter() {
    isSubmitting.value = true;
    axios
        .post(
            `${CONFIG.apiBaseUrl}${CONFIG.apiEndpoints.createDatasetFilter.replace(/{id}/g, props.dataset.id)}`,
            datasetFilterMessage(),
        )
        .then((response) => {
            if (response.status === 200) {
                submitResult.value = t("datasetFilter.submitResultOk");
            } else {
                submitResult.value = t("datasetFilter.submitResultFailed");
            }

            setTimeout(() => {
                emit("close");
                router.go();
            }, 2000);
        })
        .catch((error) => {
            throw new Error(error);
        });
}

function updateBuyerName(value) {
    buyerName.value = value;
}

function updateProcuringEntityName(value) {
    procuringEntityName.value = value;
}

watch(
    () => [
        releaseDateFrom.value,
        releaseDateTo.value,
        buyerName.value,
        procuringEntityName.value,
        buyerNameRegex.value,
        procuringEntityNameRegex.value,
    ],
    () => {
        if (filteredItemsTimeout) {
            clearTimeout(filteredItemsTimeout);
        }

        filteredItemsTimeout = setTimeout(() => datasetFilterItems(), filteredItemsTimeoutLimit);
    },
    {
        deep: true,
    },
);

onMounted(() => {
    releaseDateFrom.value = firstDate.value;
    releaseDateTo.value = lastDate.value;
    datasetFilterItems();
});
</script>

<style lang="scss">
@import "@/scss/main";

.modal_box {
    padding: 30px;
}

.modal_headline {
    padding-bottom: 30px;
}

.regex_input {
    width: 100%;
    height: 100%;
    padding-right: 0px;
    font-size: 13px;
    font-family: $font-family-mono;
}

.modal_input {
    font-weight: 400;
    line-height: 1.5;
    color: #212529;
}

.submit_button {
    font-size: 18px;
    font-weight: 700;
    color: $text-color;
    font-family: $font-family-sans-serif;
    background-color: transparent;
    border: 1px solid $na_color;
    margin-top: 20px;
}

.submit_button:hover {
    background-color: $na_color;
    color: white;
    border: 1px solid $na_color;
}

.procuring_row {
    padding-top: 15px;
}

.section_row {
    padding-top: 30px;
}

.multiselect__tag-icon:after {
    content: "×";
    color: white;
    font-size: 16px;
}

.multiselect__tag-icon:focus,
.multiselect__tag-icon:hover {
    background: $gray-800;
}
</style>
