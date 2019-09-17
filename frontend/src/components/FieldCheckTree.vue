<template>
    <table class="table table-hover tree">
        <thead>
            <tr class="d-flex">
                <th class="col">
                    <b-row class="align-items-center h-100"><b-col>Field</b-col></b-row>
                </th>
                <th class="col">
                    {{ $t('fieldDetail.coverage.label') }}

                    <b-row>
                        <b-col cols="3">{{ $t("resourceLevel.ok") }}</b-col>
                        <b-col cols="3">{{ $t("resourceLevel.failed") }}</b-col>
                        <b-col cols="6"></b-col>
                    </b-row>
                </th>
                <th class="col">
                    {{ $t('fieldDetail.quality.label') }}

                    <b-row>
                        <b-col cols="3">{{ $t("resourceLevel.ok") }}</b-col>
                        <b-col cols="3">{{ $t("resourceLevel.failed") }}</b-col>
                        <b-col cols="6"></b-col>
                    </b-row>
                </th>
            </tr>
        </thead>
        <tbody>
            <FieldCheckTreeNode v-for="n in tree" :key="n._path" :data="n" v-on:field-check-detail="reemitDetailEvent"/>
        </tbody>
    </table>
</template>

<script>
import FieldCheckTreeNode from "@/components/FieldCheckTreeNode.vue";

export default {
    data: function() {
        return {
        };
    },
    props: ["stats"],
    components: { FieldCheckTreeNode },
    computed: {
        tree: function() {
            var root = {}
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
        reemitDetailEvent: function(path) {
            this.$emit('field-check-detail', path)
        }
    }
};
</script>

<style scoped lang="scss">
@import "src/scss/main";

</style>