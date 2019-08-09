<template>
    <div class="resource">
        <h3>{{ $t("header").toUpperCase() }}</h3>
        <h2>{{ $t("sections.resource") }}</h2>
        <h4>ALL RESOURCE LEVEL CHECKS</h4>
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
                    <span v-for="name in sections">
                        <ResourceLevelList :section="name" />
                    </span>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import ResourceLevelList from "@/components/ResourceLevelList.vue";

export default {
    name: "resource",
    data: function() {
        return {
            sections: ["reference", "consistent", "coherent"]
        };
    },
    components: {
        ResourceLevelList
    }
};
</script>
