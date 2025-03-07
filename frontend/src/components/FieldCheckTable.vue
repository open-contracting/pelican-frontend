<template>
  <div>
    <div class="thr row">
      <div
        class="th col col-4"
        @click="sortByPath(tableData)"
      >
        <SortButtons
          :label="$t('field.table.head.object')"
          :active="sortedBy == 'path'"
          :asc="isAscendingSorted"
          :on-asc="() => sortByPath(tableData)"
          :on-desc="() => sortByPath(tableData, false)"
        />
      </div>
      <div
        class="th col col-4 justify-content-center d-flex"
        @click="sortByCoverage(tableData)"
      >
        <SortButtons
          :label="$t('field.table.head.coverage')"
          :active="sortedBy == 'coverage'"
          :asc="isAscendingSorted"
          :on-asc="() => sortByCoverage(tableData)"
          :on-desc="() => sortByCoverage(tableData, false)"
        />
      </div>
      <div
        class="th col col-4 justify-content-center d-flex"
        @click="sortByQuality(tableData)"
      >
        <SortButtons
          :label="$t('field.table.head.quality')"
          :active="sortedBy == 'quality'"
          :asc="isAscendingSorted"
          :on-asc="() => sortByQuality(tableData)"
          :on-desc="() => sortByQuality(tableData, false)"
        />
      </div>
    </div>

    <template v-for="n in tableData">
      <FieldCheckTableRow
        v-if="isSearched(n)"
        :key="n.path"
        :check="n"
      >
        <span v-html="highlightSearch(n.path)" />
        <template v-if="hasHidden(n)">
          <div>
            <span
              class="hide_button"
              @click.stop="switchHidden(n)"
            >
              <font-awesome-icon
                icon="eye-slash"
                class="hidden_icon"
              />
              <i>{{ $t("field.hidden", { n: n._hidden.length }) }}</i>
            </span>
          </div>
        </template>
      </FieldCheckTableRow>
      <template v-for="h in n._hidden">
        <FieldCheckTableRow
          v-if="isSearched(h)"
          :key="h.path"
          :check="h"
          :class="['hidden_row', { hidden: isHidden(n) }]"
        >
          <span v-html="highlightSearch(h.path)" />
        </FieldCheckTableRow>
      </template>
    </template>
  </div>
</template>

<script>
import FieldCheckTableRow from "@/components/FieldCheckTableRow.vue";
import SortButtons from "@/components/SortButtons.vue";
import fieldCheckMixins from "@/plugins/fieldCheckMixins.js";

export default {
    components: { FieldCheckTableRow, SortButtons },
    mixins: [fieldCheckMixins],
    props: ["filter"],
    data: () => ({
        showHidden: {},
    }),
    computed: {
        stats: function () {
            return this.$store.getters.fieldLevelStats;
        },
        tableData: function () {
            if (!this.stats) {
                return [];
            }
            const data = [];

            this.sortBy(this.stats, "path");

            for (const n of this.stats) {
                if (n.coverage.total_count && this.filter(n)) {
                    data.push(n);
                }
            }

            return data;
        },
        sortedBy: function () {
            const value = this.$store.getters.fieldCheckSortedBy;
            return value == null ? "processingOrder" : value;
        },
        isAscendingSorted: function () {
            const value = this.$store.getters.fieldCheckSortedAscending;
            return value == null ? true : value;
        },
    },
    mounted: function () {
        this.$on("field-check-table-sort", (data) => this.$store.commit("setFieldCheckSorting", data));

        this.sortBy(this.tableData, this.sortedBy, this.isAscendingSorted);
    },
    methods: {
        hasHidden: (check) => "_hidden" in check && check._hidden.length > 0,
        switchHidden: function (check) {
            const patch = {};
            patch[check.path] = !this.showHidden[check.path];
            this.showHidden = Object.assign({}, this.showHidden, patch);
        },
        isHidden: function (check) {
            return !this.showHidden[check.path];
        },
        resetSorting: function () {
            this.sortByProcessingOrder(this.tableData);
        },
        isSearched: function (check) {
            return check && this.isPathSearched(check.path);
        },
    },
};
</script>

<style scoped lang="scss">
@import "src/scss/main";
.hide_button {
    color: $na_color;
    font-size: 10px;
}

.hide_button:hover {
    color: $text-color;
}

.hidden_icon {
    position: relative;
    top: -1px;
}

.hidden {
    display: none !important;
}

.hidden_row {
    color: $na_color;
    border-left: 2px solid $na_light_color;
    background-color: #f9f9f9;
}
</style>
