<template>
    <main role="main" class="dataset main_content col-11 col-sm-10 col-md-9 col-lg-9 col-xl-10 offset-1 offset-sm-2 offset-md-3 offset-lg-3 offset-xl-2">
        <h3>{{ $t("header").toUpperCase() }}</h3>
        <h2>{{ $t("sections.dataset") }}</h2>
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
    </main>
</template>

<script>
import Loader from "@/components/Loader.vue";
export default {
    name: "dataset",
    components: { Loader },
    computed: {
        loaded() {
            if (this.$store.getters.datasetLevelStats != null) {
                return true;
            }
            return false;
        }
    }
};
</script>
