<template>
  <div
    ref="bar"
    class="inline_bar numeric"
    :class="state"
  >
    <div
      class="bar"
      :style="{ width: barWidth + 'px' }"
    >
      <span v-if="barWidth > 30">{{ percentage | formatPercentage }}</span>
      <span v-else>&nbsp;</span>
    </div>
    <div
      v-if="barWidth <= 30"
      class="count"
    >
      <span
        v-if="barWidth <= 30"
        class="small_label"
      >{{ percentage | formatPercentage }}</span>
      <span
        v-if="showCount"
        class="count_holder"
      >
        <span class="count_holder">({{ count | formatNumber }})</span>
      </span>
    </div>
    <div
      v-if="barWidth > 30 && showCount"
      class="count"
    >
      <span class="count_holder">({{ count | formatNumber }})</span>
    </div>
  </div>
</template>

<script>
export default {
    props: ["percentage", "count", "state", "showCount"],
    data: () => ({
        barWidth: 1,
    }),
    mounted() {
        if (this.percentage > 0) {
            if (this.showCount) {
                this.barWidth = ((this.$refs.bar.clientWidth - 100) / 100) * this.percentage;
            } else {
                this.barWidth = (this.$refs.bar.clientWidth / 100) * this.percentage;
            }
        }
    },
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
    color: $na_color;
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
    border-radius: 8px;
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
