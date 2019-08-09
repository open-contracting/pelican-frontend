<template>
    <div class="inline_bar" v-bind:class="state" ref="bar">
        <div class="bar" v-bind:style="{ width: barWidth + 'px' }">
            <span v-if="barWidth > 30">{{ percentage | formatNumber}}%</span>
            &nbsp;
        </div>
        <div class="count">
            <span class="small_label" v-if="barWidth <= 30">{{ percentage | formatNumber}}%</span>
            <span class="count_holder">({{ count | formatNumber}})</span>
        </div>
    </div>
</template>

<script>
export default {
    data: function() {
        return {
            barWidth: 0
        };
    },
    props: ["percentage", "count", "state"],
    mounted() {
        this.barWidth =
            ((this.$refs.bar.clientWidth - 100) / 100) * this.percentage;
    }
};
</script>

<style scoped lang="scss">
@import "src/scss/variables";
.inline_bar {
    width: 100%;
    text-align: left;
    display: inline-block;
}

.count {
    display: inline-block;
    height: 25px;
    color: $na_light_color;
    font-size: 13px;
    padding-top: 5px;
}

.count_holder {
    padding-left: 10px;
}

.bar {
    display: inline-block;
    height: 25px;
    font-size: 13px;
    padding-top: 5px;
    padding-left: 5px;
    font-weight: 700;
}

.ok .bar {
    background-color: $ok_color;
    color: white;
}

.failed .bar {
    background-color: $failed_color;
    color: white;
}

.na .bar {
    background-color: $na_bar_color;
}

.small_label {
    font-weight: 700;
    color: $text-color;
    padding-left: 5px;
}
</style>