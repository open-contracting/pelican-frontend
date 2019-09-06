<template>
    <div class="overview_card">
        <slot name="title">
            <h4 v-if="title">
                {{ title }}
                <span v-if="info" class="info" :title="info">i</span>
            </h4>
        </slot>
        <div :class="['content', 'result_box', {'blank': blank}]">
            <div class="row">
            <div class="col-11 mx-auto"><slot></slot></div>            
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "overview-card",
    props: {
        title: String,
        blank: Boolean,
        info: String
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
    margin-top: 20px;
    white-space: nowrap;
}

.info {
    color: $headings_light_color;
    cursor: pointer;
    margin-left: 20px;
}

.info:hover {
    color: $text_color;
}    
</style>