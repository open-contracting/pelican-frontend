<template>
    <span class="tree_node">
        <tr class="node_head d-flex clickable" @click="expanded = !expanded">            
            <td class="col-12">
                <div :class="'indent-' + depth" />
                <div class="switcher text-center">
                    <font-awesome-icon v-if="!expanded" icon="chevron-right" />
                    <font-awesome-icon v-else icon="chevron-down" />
                </div>
                {{ data._path.substring(data._path.lastIndexOf('.') + 1) }}
            </td>
        </tr>
        <template v-if="expanded">
            <template v-if="data._check">
                <tr class="node_data d-flex clickable" @click="$emit('field-check-detail', data._path)">                    
                    <td class="col-4 path"><div :class="'indent-' + (depth + 1)" />{{ data._path }}</td>
                    
                    <td class="col">{{ data._check.coverage.passed_count }}</td>
                    <td class="col">{{ data._check.coverage.failed_count }}</td>
                    <td class="col-2"><ProgressBar :ok="data._check.coverageOkShare" :failed="data._check.coverageFailedShare"/></td>
                    
                    <td class="col">{{ data._check.quality.passed_count }}</td>
                    <td class="col">{{ data._check.quality.failed_count }}</td>
                    <td class="col-2"><ProgressBar :ok="data._check.qualityOkShare" :failed="data._check.qualityFailedShare"/></td>
                </tr>
            </template>

            <span v-if="hasChildren" class="node_children">
                <template v-for="n in children">                
                    <tree-node :key="n._path" :data="n" :depth="depth + 1" v-on:field-check-detail="reemitDetailEvent"/>
                </template>
            </span>
        </template>
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
        reemitDetailEvent: function(path) {
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

.switcher {
    display: inline-block;
    font-size: 80%;
    width: 30px;
    color: $primary;
}

.node_data {
    td {
        border-top: none;

        &.path {
            color: $headings_light_color;
            font-family: $font-family-thin;
        }
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