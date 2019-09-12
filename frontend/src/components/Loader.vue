<template>
    <div class="result_box loader text-center">
        <div class="spinner">
            <b-spinner variant="primary" style="width: 4rem; height: 4rem;" type="grow" class="spinner"></b-spinner>
        </div>
        {{ $t("loader.generic") }}
    </div>
</template>

<script>
export default {
    data: function() {
        return {};
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