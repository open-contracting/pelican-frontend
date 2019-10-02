<template>
    <div class="container-fluid" id="app">
        <router-view />
    </div>
</template>

<script>
export default {
    data: function() {
        return {};
    },
    mounted() {
        var datasetId = this.$store.getters.datasetId;
        if (datasetId === null) {
            this.$router.push({
                name: "home",
                params: {}
            });
        }
    }
};
</script>