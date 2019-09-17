<template>
    <span v-if="resourceLevelStats.length > 0">
        <tr class="d-flex clickable" v-on:click="showChecks = !showChecks">
            <td class="col-5 category" scope="col">
                <div class="switcher text-center" v-if="!showChecks">
                    <font-awesome-icon icon="chevron-right" />
                </div>
                <div class="switcher text-center" v-if="showChecks">
                    <font-awesome-icon icon="chevron-down" />
                </div>
                {{ $t("resourceLevel." + section + ".categoryName") }}
            </td>
            <td class="col-7 text-left info_message" scope="col" span="7">{{ resourceLevelStats.length }} checks in total with avg score {{ avgScore }}%</td>
        </tr>
        <span class="checks" v-if="showChecks">
            <ResourceLevelRow v-for="(value, name, index) in resourceLevelStats" :check="value" :name="value.name" v-bind:key="name" v-bind:index="index"></ResourceLevelRow>
        </span>
    </span>
</template>

<script>
import ResourceLevelRow from "@/components/ResourceLevelRow";

export default {
    data: function() {
        return {
            showChecks: false
        };
    },
    props: ["section"],
    components: { ResourceLevelRow },
    computed: {
        resourceLevelStats() {
            var result = this.$store.getters.resourceLevelStatsBySection(
                this.section
            );
            return result;
        },
        avgScore() {
            var sum = 0;
            for (var item in this.resourceLevelStats) {
                var check = this.resourceLevelStats[item];
                sum =
                    sum +
                    check.passed_count /
                        ((check.passed_count +
                            check.failed_count +
                            check.undefined_count) /
                            100);
            }

            return Math.round(sum / this.resourceLevelStats.length);
        }
    }
};
</script>

<style scoped lang="scss">
@import "src/scss/variables";

.info_message {
    color: $na_color;
    font-weight: 300;
}

.switcher {
    display: inline-block;
    font-size: 80%;
    width: 30px;
    color: $primary;
}

.category {
    font-weight: 700;
}
</style>