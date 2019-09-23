<template>
    <dashboard>
        <h3>{{ $t("header") }}</h3>
        <h2>{{ $t("sections.resource") }}</h2>
        <span v-if="loaded">
            <h4>{{ $t("resourceLevel.subheadline") }}</h4>
            <div class="result_box">
                <table class="table table-hover">
                    <thead>
                        <tr class="d-flex">
                            <th class="col-5" scope="col">{{ $t("resourceLevel.check") }}</th>
                            <th class="col-1 text-center" scope="col">{{ $t("resourceLevel.ok") }}</th>
                            <th class="col-1 text-center" scope="col">{{ $t("resourceLevel.failed") }}</th>
                            <th class="col-1 text-center" scope="col">{{ $t("resourceLevel.na") }}</th>
                            <th class="col-1" scope="col">&nbsp;</th>
                            <th class="col-3" scope="col">&nbsp;</th>
                        </tr>
                    </thead>
                    <tbody>
                        <span v-for="(name, index) in sections" v-bind:key="index">
                            <ResourceLevelList :section="name" />
                        </span>
                    </tbody>
                </table>
            </div>
        </span>
        <span v-else>
            <Loader></Loader>
        </span>
    </dashboard>
</template>

<script>
import ResourceLevelList from "@/components/ResourceLevelList.vue";
import Loader from "@/components/Loader.vue";
import Dashboard from "@/views/layouts/Dashboard.vue";

export default {
    name: "resource",
    data: function() {
        return {
            sections: ["reference", "consistent", "coherent"]
        };
    },
    components: {
        ResourceLevelList,
        Loader,
        Dashboard
    },
    computed: {
        loaded() {
            if (this.$store.getters.resourceLevelStats != null) {
                return true;
            }
            return false;
        }
    }
};
</script>
