<template>
    <table class="table table-borderless tree">
        <thead>
            <th>
                <div class="d-flex align-items-center">
                    <div>{{ $t('field.table.head.object') }}</div>
                </div>
            </th>
            <th colspan="4" @click="sortByCoverage()">
                <div class="d-flex align-items-center">
                    <span>{{ $t('field.table.head.coverage') }}</span>
                </div>
            </th>
            <th colspan="4" @click="sortByQuality()">
                <div class="d-flex align-items-center">
                    <span>{{ $t('field.table.head.quality') }}</span>
                </div>
            </th>
        </thead>
        
        <FieldCheckTreeNode v-for="n in tree" :key="n._path" :data="n" v-on:field-check-detail="emitDetailEvent"/>
    </table>
</template>

<script>
import FieldCheckTreeNode from "@/components/FieldCheckTreeNode.vue";
import fieldCheckMixins from "@/plugins/fieldCheckMixins.js";

export default {
    data: function() {
        return {
        };
    },    
    components: { FieldCheckTreeNode },
    mixins: [fieldCheckMixins],
    computed: {
        stats: function() {
            return this.$store.getters.fieldLevelStats
        },
        tree: function() {
            var root = {}
            
            this.sortByProcessingOrder(this.stats)

            this.stats.forEach(function(n) {
                var node = root
                n.path.split(".").forEach(function(p) {
                    if (!node.hasOwnProperty(p)) {
                        node[p] = { "_path": (node._path ? node._path + "." : "") + p }
                    }                    
                    node = node[p]
                })

                node["_check"] = n
            })

            return root
        }
    },
    methods: {
        emitDetailEvent: function(path) {
            this.$emit('field-check-detail', path)
        }
    }
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