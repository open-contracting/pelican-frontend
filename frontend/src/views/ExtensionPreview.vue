<template>
    <div v-if="loaded">
        <!-- <h5>{{ $t("extension.metadata") }}</h5> -->
        <vue-json-pretty :highlightMouseoverNode="true" :deep="2" :data="extensionData"></vue-json-pretty>
    </div>
</template>

<script>
import VueJsonPretty from "vue-json-pretty";

export default {
    name: "extensionPreview",
    components: {
        VueJsonPretty,
    },
    computed: {
        loaded() {
            if (this.$store.getters.dataset != null) {
                return true;
            }
            return false;
        },
        extensionData(){
           return this.$store.getters.extensionDataByName(
                this.$route.params.extensionName
            );    
        }
    }
};
</script>
