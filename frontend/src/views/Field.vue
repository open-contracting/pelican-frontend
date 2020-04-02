<template>
    <dashboard>
        <h2>{{ $t("field.title") }}</h2>
        <div class="description" v-html=" $t('field.description')"></div>

        <h4>{{ $t('field.all') }}</h4>

        <b-row class="action_bar">
            <b-col class="text-left">
                <SearchInput :placeholder="$t('field.search')" :preset="search" :on-update="(search) => $store.commit('setFieldCheckSearch', search)" />
            </b-col>
            <b-col class="text-right">
                <b-button-group v-if="layout == 'table'">
                    <button @click="resetTableSorting()" :class="['btn', 'reset-table-sorting']">
                        <font-awesome-icon icon="sort-numeric-down" />
                    </button>
                </b-button-group>

                <b-button-group>
                    <button @click="$store.commit('setFieldCheckLayout', 'table')" :class="['btn', {active: layout == 'table'}]">
                        <font-awesome-icon icon="bars" />
                    </button>
                    <button @click="$store.commit('setFieldCheckLayout', 'tree')" :class="['btn', {active: layout == 'tree'}]">
                        <font-awesome-icon icon="align-right" />
                    </button>
                </b-button-group>
            </b-col>
        </b-row>

        <div class="field_result_box">
            <FieldCheckTable v-if="layout == 'table'" ref="field-check-table" />
            <FieldCheckTree v-else-if="layout == 'tree'" ref="field-check-tree" />
        </div>
    </dashboard>
</template>

<script>
import Dashboard from "@/views/layouts/Dashboard.vue";
import FieldCheckTable from "@/components/FieldCheckTable.vue";
import FieldCheckTree from "@/components/FieldCheckTree.vue";
import SearchInput from "@/components/SearchInput.vue";

export default {
    name: "field",
    data: function() {
        return {};
    },
    components: { Dashboard, FieldCheckTable, FieldCheckTree, SearchInput },
    computed: {
        layout: function() {
            return this.$store.getters.fieldCheckLayout;
        },
        search: function() {
            return this.$store.getters.fieldCheckSearch;
        }
    },
    methods: {
        resetTableSorting: function() {
            this.$refs["field-check-table"].resetSorting();
        }
    }
};
</script>

<style lang="scss">
@import "src/scss/_variables";

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
</style>

<style scoped lang="scss">
@import "src/scss/main";

.action_bar {
    margin-top: 15px;
    margin-bottom: 15px;

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
