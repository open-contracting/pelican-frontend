<template>
    <span class="tree_node">
        <tr class="node_head d-flex clickable">
            <td class="col-4" @click="check && emitDetailEvent(path)">
                <div class="d-flex flex-row align-items-center">
                    <div :class="'indent-' + depth" />
                    <div v-if="hasChildren" class="switcher text-center" @click.stop="expanded = !expanded">
                        <template v-if="hasChildren">
                            <font-awesome-icon v-if="!expanded" icon="chevron-right" />
                            <font-awesome-icon v-else icon="chevron-down" />
                        </template>
                    </div>
                    <div v-else class="switcher"></div>
                    <div class="name flex-fill">{{ path.substring(path.lastIndexOf('.') + 1) }}</div>
                </div>
            </td>

            <template v-if="check">
                <td class="col">{{ check.coverage.passed_count }}</td>
                <td class="col">{{ check.coverage.failed_count }}</td>
                <td class="col-2"><ProgressBar :ok="check.coverageOkShare" :failed="check.coverageFailedShare"/></td>
                
                <td class="col">{{ check.quality.passed_count }}</td>
                <td class="col">{{ check.quality.failed_count }}</td>
                <td class="col-2"><ProgressBar :ok="check.qualityOkShare" :failed="check.qualityFailedShare"/></td>
            </template>
            <td v-else class="col-8"></td>
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
            this.expanded = true
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
        },
        expanded: {
            get: function() {
                return this.$store.getters.isFieldCheckExpanded(this.path)
            },
            set: function(value) {
                if (value) {
                    this.$store.commit('addFieldCheckExpandedNode', this.path)
                } else {
                    this.$store.commit('removeFieldCheckExpandedNode', this.path)                    
                }
            }
        },
        path: function() {
            return this.data._path
        },
        check: function() {
            return this.data._check
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