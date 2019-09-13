<template>
    <div>
        <FieldCheckTreeNode v-for="n in tree" :key="n._path" :data="n" expand />
    </div>
</template>

<script>
import ProgressBar from "@/components/ProgressBar.vue";
import FieldCheckTreeNode from "@/components/FieldCheckTreeNode.vue";

export default {
    data: function() {
        return {
            
        };
    },
    props: ["stats"],
    components: { ProgressBar, FieldCheckTreeNode },
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
    }
};
</script>

<style scoped lang="scss">
@import "src/scss/main";

</style>