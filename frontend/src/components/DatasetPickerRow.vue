<template>
  <div>
    <div
      :class="['row', 'tr', 'align-items-center']"
    >
      <div class="td col-4">
        <span v-if="depth > 0" :style="{'padding-left': depth / 2 + 'rem'}">
          <font-awesome-icon :icon="['fas', 'long-arrow-alt-right']" />
        </span>
        <b-link :to="{ name: 'overview', params: { datasetId: dataset.id } }" :disabled="!isDatasetImported(dataset)">
          {{ dataset.name }}
        </b-link>
        <span class="dataset_id">(Id {{ dataset.id }})</span>
        <a
          v-if="isDatasetImported(dataset) && depth == 0"
          href="#"
          @click.stop.prevent="$emit('dataset-filter', dataset)"
        >
          <font-awesome-icon :icon="['fas', 'filter']" />
        </a>
        <a
          v-if="isDatasetImported(dataset)"
          href="#"
          @click.stop.prevent="$emit('dataset-report', dataset)"
        >
          <font-awesome-icon :icon="['fas', 'file']" />
        </a>
      </div>
      <div class="td col-1 numeric text-right">
        {{ dataset.meta.compiled_releases?.total_unique_ocids | formatNumber }}
      </div>
      <div class="td col-1 numeric text-right">
        {{ dataset.meta.kingfisher_metadata?.collection_id }}
      </div>
      <div class="td col-1 phase_cell align-items-center align-middle">
        <template v-if="dataset.phase == 'CHECKED' && dataset.state == 'OK'">
          <span class="small_icon">
            <font-awesome-icon
              :icon="['far', 'check-circle']"
              class="text-success"
            />
          </span>
          {{ dataset.phase }}
        </template>
        <template v-else-if="dataset.phase == 'DELETED' && dataset.state == 'OK'">
          <span class="small_icon">
            <font-awesome-icon
              :icon="['fas', 'ban']"
              class="text-danger"
            />
          </span>
          {{ dataset.phase }}
        </template>
        <template v-else-if="dataset.state == 'FAILED'">
          <span class="small_icon">
            <font-awesome-icon
              :icon="['far', 'times-circle']"
              class="text-danger"
            />
          </span>
          {{ dataset.phase }}
        </template>
        <template v-else>
          <b-row class="progress_label no-gutters">
            <b-col
              v-for="p in phases"
              :key="p"
            >
              <template v-if="p == dataset.phase">
                {{ p }}
              </template>
            </b-col>
          </b-row>

          <ProgressBar :value="getDatasetProgress(dataset)" />
        </template>
      </div>
      <div class="td col numeric">
        <span class="created">{{ dataset.created }}</span>
        <br>
        <span class="modified">{{ dataset.modified }}</span>
      </div>
      <div class="td col">
        <b-link
          v-if="dataset.ancestor_id"
          class="time_variance break_word"
          :title="dataset.ancestor_id"
          @click.stop="setDataset(dataset, { name: 'time' })"
        >
          <span class="small_icon">
            <font-awesome-icon icon="history" />
          </span>
          {{ dataset.ancestor_name }} (Id {{ dataset.ancestor_id }})
        </b-link>
      </div>
    </div>
    <template v-for="(item, index) in dataset.filtered_children">
      <DatasetPickerRow
        :key="index"
        :dataset="item"
        :depth="depth + 1"
        @dataset-filter="$emit('dataset-filter', $event)"
        @dataset-report="$emit('dataset-report', $event)"
      />
    </template>
  </div>
</template>

<script>
import ProgressBar from "@/components/ProgressBar.vue";
import sortMixins from "@/plugins/sortMixins.js";
import stateMixin from "@/plugins/stateMixins.js";

export default {
    name: "DatasetPickerRow",
    components: { ProgressBar },
    mixins: [stateMixin, sortMixins],
    props: ["dataset", "depth"],
    data: () => ({
        showFilteredChildren: false,
    }),
    computed: {
        phases: () => ["PLANNED", "CONTRACTING_PROCESS", "DATASET", "TIME_VARIANCE", "CHECKED"],
    },
    methods: {
        getDatasetProgress: function (dataset) {
            return (this.phases.indexOf(dataset.phase) + 1) * 20;
        },
        isDatasetImported: (dataset) => dataset.phase === "CHECKED" && dataset.state === "OK",
    },
};
</script>

<style scoped lang="scss">
@import "src/scss/main";

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

.tr {
    a.disabled {
        pointer-events: none;
        color: $gray-600;
        text-decoration: none;
        &:hover {
            text-decoration: none;
        }
    }
}

.th {
    .modified {
        font-family: $font-family-thin;
        color: $headings_light_color;
    }
}

.td {
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
