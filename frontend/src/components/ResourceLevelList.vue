<template>
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
            <ResourceLevelRow v-for="(value, name, index) in resourceLevelStats" :check="value" :name="name" v-bind:key="name" v-bind:index="index"></ResourceLevelRow>
        </tbody>
    </table>
</template>

<script>
import ResourceLevelRow from "@/components/ResourceLevelRow";

export default {
    data: function() {
        return {};
    },
    components: { ResourceLevelRow },
    computed: {
        resourceLevelStats() {
            return this.$store.getters.resourceLevelStats;
        }
    }
};
</script>

<style scoped lang="scss">
</style>