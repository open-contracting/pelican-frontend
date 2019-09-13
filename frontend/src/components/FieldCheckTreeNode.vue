<template>
    <div class="tree_node">
        <div @click="expanded = !expanded">{{ data._path }}</div>
        <div class="expandable" v-if="expanded">
            <div v-if="data._check">
                {{ $t('fieldDetail.coverage.label') }}: {{ data._check.coverage.passed_count }} / {{ data._check.coverage.failed_count }} / {{ data._check.coverage.total_count }}<br/>
                {{ $t('fieldDetail.quality.label') }}: {{ data._check.quality.passed_count }} / {{ data._check.quality.failed_count }} / {{ data._check.quality.total_count }}
            </div>
            <template v-for="(n, k) in data">
                <tree-node v-if="!k.startsWith('_')" :key="n._path" :data="n" />
            </template>
        </div>
    </div>
</template>

<script>
import ProgressBar from "@/components/ProgressBar.vue";

export default {
    data: function() {
        return {
            expanded: false
        };
    },
    props: {
        data: Object,
        expand: Boolean
    },
    name: "tree-node",
    components: { ProgressBar },
    mounted: function() {
        if (this.expand) {
            this.expanded = true;
        }
    },
    computed: {
    }
};
</script>

<style scoped lang="scss">
@import "src/scss/main";

.tree_node {
    margin-left: 1em;
}
</style>