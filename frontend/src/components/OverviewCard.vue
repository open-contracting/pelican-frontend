<template>
    <div class="overview_card">
        <h4 v-if="title">{{ title }}</h4>
        <div :class="['content', 'result_box', {'blank': blank}]">
            <slot></slot>
        </div>
    </div>
</template>

<script>
export default {
    name: "overview-card",
    props: {
        title: String,
        blank: Boolean
    }
};
</script>

<style scoped lang="scss">
@import "src/scss/main";
.blank {
    background-color: transparent;
    border: none;
}

h4 {
    margin-bottom: 20px;
    margin-top: 20px
}

.table {
    margin: 0;
}
</style>