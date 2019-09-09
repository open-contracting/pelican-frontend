<template>
    <div class="progress_bar">
        <div class="inner" :style="{width: value + '%'}"></div>
    </div>
</template>

<script>
export default {
    name: "overview-card",
    props: ["value"]
};
</script>

<style scoped lang="scss">
@import "src/scss/main";

.progress_bar {
    width: 100%;
    height: 5px;
    background-color: $na_color;
    display: inline-block;
    position: relative;
    border-radius: 2.5px;

    .inner {
        background-color: $primary;
        height: 5px;
        display: inline-block;
        position: absolute;
        top: 0;
        left: 0;
        border-radius: 2.5px;
    }
}
</style>