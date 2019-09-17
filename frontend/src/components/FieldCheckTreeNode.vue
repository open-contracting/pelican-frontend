<template>
    <span class="tree_node">
        <tr class="node_head d-flex clickable">
            <td class="col-4" @click="emitDetailEvent(data._path)">
                <div class="d-flex flex-row align-items-center">
                    <div :class="'indent-' + depth" />
                    <div v-if="hasChildren" class="switcher text-center" @click.stop="expandChildren">
                        <template v-if="hasChildren">
                            <font-awesome-icon v-if="!expanded" icon="chevron-right" />
                            <font-awesome-icon v-else icon="chevron-down" />
                        </template>
                    </div>
                    <div v-else class="switcher"></div>
                    <div class="name flex-fill">{{ data._path.substring(data._path.lastIndexOf('.') + 1) }}</div>
                </div>
            </td>

            <template v-if="data._check">
                <td class="col">{{ data._check.coverage.passed_count }}</td>
                <td class="col">{{ data._check.coverage.failed_count }}</td>
                <td class="col-2"><ProgressBar :ok="data._check.coverageOkShare" :failed="data._check.coverageFailedShare"/></td>
                
                <td class="col">{{ data._check.quality.passed_count }}</td>
                <td class="col">{{ data._check.quality.failed_count }}</td>
                <td class="col-2"><ProgressBar :ok="data._check.qualityOkShare" :failed="data._check.qualityFailedShare"/></td>
            </template>
        </tr>

        <span v-if="hasChildren && expanded" class="node_children">
            <template v-for="n in children">                
                <tree-node :key="n._path" :data="n" :depth="depth + 1" v-on:field-check-detail="emitDetailEvent"/>
            </template>
        </span>
    </span>
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
        expand: Boolean,
        depth: {type: Number, default: 0}
    },
    name: "tree-node",
    components: { ProgressBar },
    mounted: function() {
        if (this.expand) {
            this.expanded = true;
        }
    },
    computed: {
        children: function() {
            var result = Object.assign({}, this.data)
            delete result._check
            delete result._path
            return result
        },
        hasChildren: function() {
            return Object.keys(this.children).length > 0
        }
    },
    methods: {
        emitDetailEvent: function(path) {
            this.$emit('field-check-detail', path)
        },
        expandChildren: function() {
            this.expanded = !this.expanded
        }
    }
};
</script>

<style scoped lang="scss">
@import "src/scss/main";

$indent-width-px: 35px;

@function indent-with($depth) {
    @return ($depth * $indent-width-px);
}

.node_head {
    .switcher {
        display: inline-block;
        font-size: 80%;
        width: 30px;
        color: $primary;
        position: relative;
    }

    .name {
        display: inline-block;
    }
}

.node_data {
    td {
        border-top: none;
    }
}

div[class^="indent-"] {
    display: inline-block;
}

@for $depth from 0 to 10 {
    .indent-#{$depth} {
        width: indent-with($depth);
    }
}
</style>