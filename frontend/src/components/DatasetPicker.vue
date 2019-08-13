<template>
    <form class="form-inline">
        <div class="form-group mb-4">
            <label for="staticEmail2">ID</label>
        </div>
        <div class="form-group mx-sm-3 mb-4">
            <input class="form-control" v-model="datasetId" type="text" required autofocus />
        </div>
        <button @click.prevent="setDatasetId" class="btn btn-primary mb-4" type="submit">GO</button>
    </form>
</template>

<script>
export default {
    data: function() {
        return {
            datasetId: "honduras_2019-08-12_15:58:04"
        };
    },
    methods: {
        setDatasetId: function() {
            this.$store.dispatch("updateDatasetId", this.datasetId);
        }
    }
};
</script>

<style scoped lang="scss">
</style>