<template>
    <fragment>
        <FieldCheckTableRow :key="path" :check="check" :class="{'d-none': hide}" @click.native="$emit('field-check-detail', path)">
            <div class="d-flex flex-row align-items-center">
                <div :class="'indent-' + depth" />
                <div v-if="hasChildren" class="switcher text-center" @click.stop="expanded = !expanded">
                    <template v-if="hasChildren">
                        <font-awesome-icon v-if="!expanded" icon="chevron-right" />
                        <font-awesome-icon v-else icon="chevron-down" />
                    </template>
                </div>
                <div v-else class="switcher"></div>
                <div class="name flex-fill" :title="path">{{ path.substring(path.lastIndexOf('.') + 1) }}</div>
            </div>
        </FieldCheckTableRow>

        <template v-if="hasChildren">
            <template v-for="n in children">                
                <tree-node :key="n._path" :data="n" :depth="depth + 1" v-on:field-check-detail="emitDetailEvent" :hide="!expanded" />
            </template>
        </template>
    </fragment>
</template>

<script>
import ProgressBar from "@/components/ProgressBar.vue";
import FieldCheckTableRow from "@/components/FieldCheckTableRow.vue";
import { VFragment } from 'vue-fragment'

export default {
    data: function() {
        return {            
        };
    },
    props: {
        data: Object,
        expand: Boolean,
        depth: {type: Number, default: 0},
        hide: {type:Boolean, default: false}
    },
    name: "tree-node",
    components: { ProgressBar, FieldCheckTableRow, VFragment },
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