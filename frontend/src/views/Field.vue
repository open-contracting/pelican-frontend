<template>
    <dashboard>
        <h3>{{ $t("header").toUpperCase() }}</h3>
        <h2>{{ $t("field.title") }}</h2>
        <div class="description">
            <p>{{ $t('field.description[0]') }}</p>
            <p>{{ $t('field.description[1]') }}</p>
            <p>{{ $t('field.description[2]') }}</p>
        </div>

        <h4>{{ $t('field.all') }}</h4>

        <b-row class="action_bar">
            <b-col class="text-left">
                <b-input-group class="search_input">
                    <template v-slot:prepend>
                        <b-input-group-text>
                            <font-awesome-icon icon="search" />
                        </b-input-group-text>
                    </template>
                    <b-input :model="search" :placeholder="$t('field.search')"/>
                </b-input-group>
            </b-col>
            <b-col class="text-right">
                <b-button-group v-if="layout == 'table'">
                    <button @click="resetTableSorting()" :class="['btn', 'reset-table-sorting']">
                        <font-awesome-icon icon="list-ol" />
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

        <div class="result_box">
            <FieldCheckTable v-if="layout == 'table'" v-on:field-check-detail="detail" ref="field-check-table"/>
            <FieldCheckTree v-else-if="layout == 'tree'" v-on:field-check-detail="detail" ref="field-check-tree" />
        </div>
    </dashboard>
</template>

<script>
import Dashboard from "@/views/layouts/Dashboard.vue";
import FieldCheckTable from "@/components/FieldCheckTable.vue";
import FieldCheckTree from "@/components/FieldCheckTree.vue";

export default {
    name: "field",
    data: function() {
        return {
            search: null
        }
    },
    components: { Dashboard, FieldCheckTable, FieldCheckTree },
    computed: {
        layout: function() {
            return this.$store.getters.fieldCheckLayout
        }
    },
    methods: {
        detail: function(path) {
            this.$router.push({
                name: "fieldCheckDetail",
                params: { path: path }
            });
        },
        resetTableSorting: function() {
            this.$refs['field-check-table'].resetSorting()
        }
    }
};
</script>

<style scoped lang="scss">
@import "src/scss/main";

.description {
    color: $headings_light_color;
}

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

        &:hover, &.active {
            border-color: $primary;
            color: $primary;
        }
    }
}

.search_input {
    .input-group-text {
        background-color: transparent;
        border-right: none;
    }
    input {
        background-color: transparent;
        border-left: none;
    }
}
</style>
