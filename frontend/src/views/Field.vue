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
                <b-input-group>
                    <template v-slot:prepend>
                        <b-input-group-text></b-input-group-text>
                    </template>
                    <b-input :model="search" />
                </b-input-group>
            </b-col>
            <b-col class="text-right">
                <b-button-group>
                    <b-button @click="layout = 'table'">TABLE</b-button>
                    <b-button @click="layout = 'tree'">TREE</b-button>
                </b-button-group>
            </b-col>
        </b-row>

        <div class="result_box">
            <FieldCheckTable v-if="layout == 'table'" :stats="stats" v-on:field-check-detail="detail" />
            <FieldCheckTree v-else-if="layout == 'tree'" :stats="stats" v-on:field-check-detail="detail" />
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
            search: null,
            layout: "table"
        }
    },
    components: { Dashboard, FieldCheckTable, FieldCheckTree },
    computed: {
        stats: function() {
            return this.$store.getters.fieldLevelStats
        }
    },
    methods: {
        detail(path) {
            this.$router.push({
                name: "fieldCheckDetail",
                params: { path: path }
            });
        }
    }
};
</script>

<style scoped lang="scss">
@import "src/scss/main";

.description {
    color: $headings_light_color;
}

</style>
