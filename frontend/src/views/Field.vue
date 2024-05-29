<template>
  <dashboard>
    <h2>{{ $t("field.title") }}</h2>
    <div
      id="field_description"
      class="description"
      v-html="$t('field.description')"
    />

    <div class="checked_fields_box">
      <div class="checked_fields_icon">
        <font-awesome-icon
          :icon="['fas', 'hand-point-right']"
          :style="{ color: '#FDC926' }"
        />
      </div>
      <div class="checked_fields_text">
        {{ $t("field.checkedFields") }}
      </div>
    </div>

    <h4 class="sub_headline">
      {{ $t("field.all") }}
    </h4>

    <b-row
      class="action_bar"
      align-v="center"
    >
      <b-col class="text-left">
        <SearchInput
          :placeholder="$t('field.search')"
          :preset="search"
          :on-update="search => $store.commit('setFieldCheckSearch', search)"
        />
      </b-col>
      <b-col class="text-right">
        <b-button-group v-if="layout == 'table'">
          <button
            :class="['btn', 'reset-table-sorting']"
            @click="resetTableSorting()"
          >
            <font-awesome-icon icon="sort-numeric-down" />
          </button>
        </b-button-group>

        <b-button-group>
          <button
            :class="['btn', { active: layout == 'table' }]"
            @click="$store.commit('setFieldCheckLayout', 'table')"
          >
            <font-awesome-icon icon="bars" />
          </button>
          <button
            :class="['btn', { active: layout == 'tree' }]"
            @click="$store.commit('setFieldCheckLayout', 'tree')"
          >
            <font-awesome-icon icon="align-right" />
          </button>
        </b-button-group>
        <FilterDropdown
          :filter-names="filterNames"
          :start-index="filterIndex"
          @newSelectedIndex="newSelectedIndex => (filterIndex = newSelectedIndex)"
        />
      </b-col>
    </b-row>

    <div class="field_result_box">
      <FieldCheckTable
        v-if="layout == 'table'"
        ref="field-check-table"
        :filter="filters[filterIndex]"
      />
      <FieldCheckTree
        v-else-if="layout == 'tree'"
        ref="field-check-tree"
        :filter="filters[filterIndex]"
      />
    </div>
  </dashboard>
</template>

<script>
import FieldCheckTable from "@/components/FieldCheckTable.vue";
import FieldCheckTree from "@/components/FieldCheckTree.vue";
import FilterDropdown from "@/components/FilterDropdown.vue";
import SearchInput from "@/components/SearchInput.vue";
import Dashboard from "@/views/layouts/Dashboard.vue";

export default {
    name: "Field",
    components: {
        Dashboard,
        FieldCheckTable,
        FieldCheckTree,
        SearchInput,
        FilterDropdown,
    },
    data: function () {
        return {
            filterIndex: 0,
            filterNames: [
                this.$t("field.filterDropdown.all"),
                this.$t("field.filterDropdown.coverageFailedOnly"),
                this.$t("field.filterDropdown.qualityFailedOnly"),
                this.$t("field.filterDropdown.passedOnly"),
            ],
            filters: [
                () => true,
                (item) => item.coverage.failed_count > 0,
                (item) => item.quality.failed_count > 0,
                (item) =>
                    item.coverage.failed_count === 0 &&
                    item.quality.failed_count === 0 &&
                    item.coverage.passed_count > 0,
            ],
        };
    },
    computed: {
        layout: function () {
            return this.$store.getters.fieldCheckLayout;
        },
        search: function () {
            return this.$store.getters.fieldCheckSearch;
        },
    },
    watch: {
        filterIndex: function (newFilterIndex) {
            this.$store.commit("setFieldLevelFilterIndex", newFilterIndex);
        },
    },
    created() {
        this.filterIndex = this.$store.getters.fieldLevelFilterIndex;
    },
    methods: {
        resetTableSorting: function () {
            this.$refs["field-check-table"].resetSorting();
        },
    },
};
</script>

<style lang="scss">
@import "src/scss/_variables";
@import "src/scss/main";

.sub_headline {
    margin-bottom: 0px;
}

#field_description {
    margin-bottom: 30px;
}

.checked_fields_box {
    margin-bottom: 30px;
    width: 100%;
}

.checked_fields_box .checked_fields_icon {
    background-color: #dde0f6;
    border-top-left-radius: 10px;
    border-bottom-left-radius: 10px;
    border: 0;
    padding: 15px;
    padding-right: 5px;
    float: left;
}

.checked_fields_box .checked_fields_text {
    background-color: #dde0f6;
    border-top-right-radius: 10px;
    border-bottom-right-radius: 10px;
    border: 0;
    padding-top: 16px;
    padding-bottom: 14px;
    padding-right: 15px;
    vertical-align: -1px;
    color: $text-color;
    overflow: auto;
}

.field_result_box {
    background-color: white;
    border-radius: 10px;
    padding: 40px;
    box-shadow: 0 2px 18px 6px rgba(0, 0, 0, 0.06);
    border: 0;
}

mark {
    background-color: $primary !important;
}

.action_bar {
    margin-bottom: 5px;

    .btn-group {
        margin-left: 15px;
    }

    button {
        background-color: transparent;
        border-color: $text-color;
        color: $text-color;

        &:hover,
        &.active {
            border-color: $primary;
            color: $primary;
        }
    }
}
</style>
