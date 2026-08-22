<template>
  <tr>
    <td>
      <span v-if="depth > 0" :style="{'padding-left': depth / 2 + 'rem'}">
        <FontAwesomeIcon :icon="['fas', 'long-arrow-alt-right']" />
      </span>
      <BLink :to="{ name: 'overview', params: { datasetId: dataset.id } }" :disabled="!isDatasetImported(dataset)">
        {{ dataset.name }}
      </BLink>
      <span class="dataset_id">(Id {{ dataset.id }})</span>
      <a
        v-if="isDatasetImported(dataset) && depth == 0"
        href="#"
        @click.stop.prevent="$emit('dataset-filter', dataset)"
      >
        <FontAwesomeIcon :icon="['fas', 'filter']" />
      </a>
      <a
        v-if="isDatasetImported(dataset)"
        href="#"
        @click.stop.prevent="$emit('dataset-report', dataset)"
      >
        <FontAwesomeIcon :icon="['fas', 'file']" />
      </a>
    </td>
    <td class="numeric text-end">
      {{ formatNumber(dataset.meta.compiled_releases.total_unique_ocids) }}
    </td>
    <td class="numeric text-end">
      {{ dataset.meta.kingfisher_metadata?.collection_id }}
    </td>
    <td class="phase_cell align-middle">
      <template v-if="dataset.phase == 'CHECKED' && dataset.state == 'OK'">
        <span class="small_icon">
          <FontAwesomeIcon
            :icon="['far', 'check-circle']"
            class="text-success"
          />
        </span>
        {{ $t("dataset.phases." + dataset.phase) }}
      </template>
      <template v-else-if="dataset.phase == 'DELETED' && dataset.state == 'OK'">
        <span class="small_icon">
          <FontAwesomeIcon
            :icon="['fas', 'ban']"
            class="text-danger"
          />
        </span>
        {{ $t("dataset.phases." + dataset.phase) }}
      </template>
      <template v-else-if="dataset.state == 'FAILED'">
        <span class="small_icon">
          <FontAwesomeIcon
            :icon="['far', 'times-circle']"
            class="text-danger"
          />
        </span>
        {{ $t("dataset.phases." + dataset.phase) }}
      </template>
      <template v-else>
        <BRow class="progress_label g-0">
          <BCol
            v-for="p in PHASES"
            :key="p"
          >
            <template v-if="p == dataset.phase">
              {{ $t("dataset.phases." + p) }}
            </template>
          </BCol>
        </BRow>

        <ProgressBar :value="getDatasetProgress(dataset)" />
      </template>
    </td>
    <td class="numeric">
      <span class="created">{{ dataset.created }}</span>
      <br>
      <span class="modified">{{ dataset.modified }}</span>
    </td>
    <td>
      <BLink
        v-if="dataset.ancestor_id"
        class="time_variance break_word"
        :to="{ name: 'time', params: { datasetId: dataset.id } }"
      >
        <span class="small_icon">
          <FontAwesomeIcon icon="history" />
        </span>
        {{ dataset.ancestor_name }} (Id {{ dataset.ancestor_id }})
      </BLink>
    </td>
  </tr>
  <template v-for="(item, index) in dataset.filtered_children" :key="index">
    <DatasetPickerRow
      :dataset="item"
      :depth="depth + 1"
      @dataset-filter="$emit('dataset-filter', $event)"
      @dataset-report="$emit('dataset-report', $event)"
    />
  </template>
</template>

<script setup lang="ts">
import { BCol, BLink, BRow } from "bootstrap-vue-next";
import { useFormatters } from "@/composables/useFormatters";
import { PHASES } from "@/config";
import type { DatasetNode } from "@/types.js";
import ProgressBar from "./ProgressBar.vue";

const { formatNumber } = useFormatters();

defineOptions({ name: "DatasetPickerRow" });

withDefaults(
  defineProps<{
    dataset: DatasetNode;
    depth?: number;
  }>(),
  { depth: 0 },
);
defineEmits<{ "dataset-filter": [dataset: DatasetNode]; "dataset-report": [dataset: DatasetNode] }>();

function getDatasetProgress(dataset: DatasetNode) {
  return (PHASES.indexOf(dataset.phase) + 1) * 25;
}

function isDatasetImported(dataset: DatasetNode) {
  return dataset.phase === "CHECKED" && dataset.state === "OK";
}
</script>

<style scoped lang="scss">

.switcher {
    display: inline-block;
    font-size: 80%;
    width: 30px;
    color: $primary;
}

.form-control::placeholder {
    color: red;
}

.small_icon {
    position: relative;
    top: -1px;
}

.picker_table {
    padding: 30px;
}

.search_input {
    margin-bottom: 20px;
}

tr {
    a.disabled {
        pointer-events: none;
        color: $gray-600;
        text-decoration: none;
        &:hover {
            text-decoration: none;
        }
    }
}

th {
    .modified {
        font-family: $font-family-thin;
        color: $headings_light_color;
    }
}

td {
    .created {
        font-weight: 700;
    }

    .modified {
        color: $headings_light_color;
    }

    &:nth-of-type(4) {
        white-space: nowrap;
    }

    .dataset_id {
        color: $na_color;
        font-family: $font-family-thin;
        font-size: 14px;
    }
}

.phase_cell {
    font-family: $font-family-thin;

    .progress_label {
        font-size: 11px;

        .col {
            white-space: nowrap;
        }

        .state-failed {
            color: $failed_color;
        }
    }
}

.time_variance {
    font-family: $font-family-thin;
    color: $primary;
    max-width: 110px;

    svg {
        margin-right: 4px;
    }
}

.action_bar {
    margin-top: 15px;
    margin-bottom: 15px;
}
</style>
