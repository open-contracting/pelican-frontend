<template>
    <div class="inline_bar numeric" v-bind:class="state" ref="bar">
        <div class="bar" v-bind:style="{ width: barWidth + 'px' }">
            <span v-if="barWidth > 30">{{ percentage | formatNumber}}%</span>
            <span v-else>&nbsp;</span>
        </div>
        <div v-if="barWidth <= 30" class="count">
            <span class="small_label" v-if="barWidth <= 30">{{ percentage | formatNumber}}%</span>
            <span v-if="showCount" class="count_holder">
                <span>&#40;</span>
                {{ count | formatNumber}}
                <span>&#41;</span>
            </span>
        </div>
        <div v-if="barWidth > 30 && showCount" class="count">
            <span class="count_holder">
                <span>&#40;</span>
                {{ count | formatNumber}}
                <span>&#41;</span>
            </span>
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
    props: ["percentage", "count", "state", "showCount"],
    mounted() {
        if (this.showCount) {
            this.barWidth =
                ((this.$refs.bar.clientWidth - 100) / 100) * this.percentage;
        } else {
            this.barWidth =
                (this.$refs.bar.clientWidth / 100) * this.percentage;
        }
    }
};
</script>

<style scoped lang="scss">
@import "src/scss/variables";
.inline_bar {
    width: 100%;
    text-align: left;
    display: inline-block;
    position: relative;
}

.count {
    display: inline-block;
    height: 25px;
    color: $na_light_color;
    font-size: 14px;
    padding-top: 4px;
}

.count_holder {
    padding-left: 10px;
}

.bar {
    display: inline-block;
    height: 25px;
    font-size: 14px;
    padding-top: 3px;
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

.reg .bar {
    background-color: #555cb3;
    color: white;
}
</style>