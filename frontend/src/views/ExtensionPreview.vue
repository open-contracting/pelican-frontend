<template>
  <div v-if="loaded">
    <!-- <h5>{{ $t("extension.metadata") }}</h5> -->
    <vue-json-pretty
      :highlight-mouseover-node="true"
      :data="extensionData"
    />
  </div>
</template>

<script>
import VueJsonPretty from "vue-json-pretty";
import 'vue-json-pretty/lib/styles.css';

export default {
    name: "ExtensionPreview",
    components: {
        VueJsonPretty
    },
    computed: {
        loaded() {
            if (this.$store.getters.dataset != null) {
                return true;
            }
            return false;
        },
        extensionData() {
            return this.$store.getters.extensionDataByName(this.$route.params.extensionName);
        }
    }
};
</script>
