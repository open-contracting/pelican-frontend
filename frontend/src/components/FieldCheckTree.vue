<template>
    <div class="table">
        <div class="thr row">
            <div class="th col col-4">
                <div class="d-flex align-items-center">
                    <div>{{ $t('field.table.head.object') }}</div>
                </div>
            </div>
            <div class="th col col-4 justify-content-center d-flex" @click="sortByCoverage()">
                <div class="d-flex align-items-center">
                    <span>{{ $t('field.table.head.coverage') }}</span>
                </div>
            </div>
            <div class="th col col-4 justify-content-center d-flex" @click="sortByQuality()">
                <div class="d-flex align-items-center">
                    <span>{{ $t('field.table.head.quality') }}</span>
                </div>
            </div>
        </div>

        <FieldCheckTreeNode v-for="n in tree" :key="n._check.path" :data="n"/>
    </div>
</template>

<script>
import FieldCheckTreeNode from "@/components/FieldCheckTreeNode.vue";
import fieldCheckMixins from "@/plugins/fieldCheckMixins.js";

export default {
    data: function() {
        return {};
    },
    props: ["filter"],
    components: { FieldCheckTreeNode },
    mixins: [fieldCheckMixins],
    watch: {
        search: function() {
            this.$store.dispatch("setExpandedNodesForSearch");
        },
        filter: function() {
            this.$store.commit("setFieldLevelFilter", this.filter);
        }
    },
    mounted: function() {
        if (this.search) {
            this.$store.dispatch("setExpandedNodesForSearch");
        }
    },
    computed: {
        stats: function() {
            return this.$store.getters.fieldLevelStats;
        },
        tree: function() {
            var root = {};

            this.sortByProcessingOrder(this.stats);

            this.stats.forEach(function(n) {
                var node = root;
                n.path.split(".").forEach(function(p) {
                    if (!node.hasOwnProperty(p)) {
                        node[p] = {};
                    }
                    node = node[p];
                });

                node["_check"] = n;
            });

            return root;
        }
    },
};
</script>

<style scoped lang="scss">
@import "src/scss/main";

.table {
    thead {
        th {
            color: $headings_light_color;
            font-family: $headings-font-family;
        }
    }
}
</style>