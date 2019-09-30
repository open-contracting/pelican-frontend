<template>
    <dashboard>
        <h2>{{ $t("sections.resource") }}</h2>
        <span v-if="loaded">
            <h4>{{ $t("resourceLevel.subheadline") }}</h4>
            <div class="result_box">
                <div class="thr row">
                    <div class="th col-9 col-lg-5" scope="col">{{ $t("resourceLevel.check") }}</div>
                    <div class="th col-1 text-center" scope="col">{{ $t("resourceLevel.ok") }}</div>
                    <div class="th col-1 text-center" scope="col">{{ $t("resourceLevel.failed") }}</div>
                    <div class="th col-1 text-center" scope="col">{{ $t("resourceLevel.na") }}</div>
                    <div class="th col-4 d-none d-lg-block" scope="col">&nbsp;</div>
                </div>
                <span v-for="(name, index) in sections" v-bind:key="index">
                    <ResourceLevelList :section="name" />
                </span>
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
