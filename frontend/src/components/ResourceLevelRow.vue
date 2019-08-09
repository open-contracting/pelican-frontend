<template>
    <tr class="d-flex clickable" v-on:click="detail()">
        <td class="col-5">
            <span class="check_name">{{ $t("resourceLevel." + name + ".name") }}</span>
        </td>
        <td class="col-1 text-right">
            <span v-if=" okPercentage> 0" class="value_ok">{{ okPercentage }}%</span>
        </td>
        <td class="col-1 text-right">
            <span v-if=" failedPercentage> 0" class="value_failed">{{ failedPercentage }}%</span>
        </td>
        <td class="col-1 text-right">
            <span v-if=" naPercentage> 0" class="value_na">{{ naPercentage }}%</span>
        </td>
        <td class="col-1 text-right"></td>
        <td class="col-3">
            <div class="stacked_line_chart">
                <div class="ok_bar" v-bind:style="{ width: okPercentage + '%' }">&nbsp;</div>
                <div class="failed_bar" v-bind:style="{ width: failedPercentage + '%' }">&nbsp;</div>
            </div>
        </td>
    </tr>
</template>

<script>
export default {
    data: function() {
        return {};
    },
    props: ["check", "name"],
    methods: {
        onePercent: function() {
            return (this.check.ok + this.check.failed + this.check.na) / 100;
        },
        detail: function() {
            this.$router.push({
                name: "resourceCheckDetail",
                params: { check: this.name }
            });
        }
    },
    computed: {
        okPercentage() {
            return Math.round(this.check.ok / this.onePercent());
        },
        failedPercentage() {
            return Math.round(this.check.failed / this.onePercent());
        },
        naPercentage() {
            return Math.round(this.check.na / this.onePercent());
        }
    }
};
</script>

<style scoped lang="scss">
@import "src/scss/variables";

.stacked_line_chart {
    display: inline-block;
    height: 4px;
    background-color: $na_light_color;
    position: relative;
    overflow: hidden;
    width: 100%;
}

.ok_bar {
    background-color: $ok_color;
    display: inline-block;
}

.failed_bar {
    background-color: $failed_color;
    display: inline-block;
}

.check_name {
    padding-left: 35px;
}
</style>