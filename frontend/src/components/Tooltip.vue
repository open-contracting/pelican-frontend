<template>
    <span>
        <span :id="tooltipId">
            <font-awesome-icon icon="info-circle" />
        </span>
        <b-tooltip :target="tooltipId" triggers="hover">
            <span class="tooltip_text" v-html="text" />
        </b-tooltip>
    </span>
</template>

<script>
export default {
    props: ["text"],
    data: function () {
        return {};
    },
    computed: {
        tooltipId: function () {
            var id = "id-" + Math.floor(Math.random() * 10000000000);

            return id;
        }
    }
};
</script>

<style scoped lang="scss">
.loader {
    font-size: 19px;
    font-weight: 700;
    padding: 40px;
}

.spinner {
    margin-bottom: 40px;
    font-size: 40px;
}
</style>
