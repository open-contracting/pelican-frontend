<template>
  <div class="progress_bar">
    <template v-for="(b, i) in allBars">
      <div
        v-if="b.value"
        :key="i"
        :class="['inner', b.class]"
        :style="{ width: b.value + '%', 'background-color': b.color }"
      >
                &nbsp;
      </div>
    </template>
  </div>
</template>

<script>
export default {
    name: "ProgressBar",
    props: ["bars", "value", "ok", "failed"],
    computed: {
        allBars: function () {
            var result = [];

            if (this.value) {
                result.push({ value: this.value });
            }
            if (this.ok) {
                result.push({ value: this.ok, class: "ok" });
            }
            if (this.failed) {
                result.push({ value: this.failed, class: "failed" });
            }
            if (this.bars) {
                result.concat(this.bars);
            }

            return result;
        }
    }
};
</script>

<style scoped lang="scss">
@import "src/scss/main";

.progress_bar {
    width: 100%;
    height: 4px;
    background-color: $na_light_color;
    display: inline-block;
    position: relative;
    overflow: hidden;
    border-radius: 2px;

    .inner {
        background-color: $primary;
        height: 4px;
        display: inline-block;

        &.ok {
            background-color: $ok_color;
        }

        &.failed {
            background-color: $failed_color;
        }
    }
}
</style>
