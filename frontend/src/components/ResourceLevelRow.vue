<template>
  <tr
    class="clickable"
    @click="detail()"
  >
    <td class="col-9 col-lg-5 break_word check_name">
      <span>{{ $t("resourceLevel." + name + ".name") }}</span>
    </td>
    <td class="col-1 col-lg-1 text-end">
      <span
        v-if="okRatio"
        class="value_ok"
      >{{ formatPercentage(okRatio) }}</span>
      <span
        v-else
        class="value_na opacity"
      >{{ formatPercentage(okRatio) }}</span>
    </td>
    <td class="col-1 col-lg-1 text-end">
      <span
        v-if="failedRatio"
        class="value_failed"
      >{{ formatPercentage(failedRatio) }}</span>
      <span
        v-else
        class="value_na opacity"
      >{{ formatPercentage(failedRatio) }}</span>
    </td>
    <td class="col-1 col-lg-1 text-end">
      <span
        v-if="naRatio"
        class="value_na"
      >{{ formatPercentage(naRatio) }}</span>
      <span
        v-else
        class="value_na opacity"
      >{{ formatPercentage(naRatio) }}</span>
    </td>
    <td class="col-4 d-none d-lg-table-cell progress_column">
      <ProgressBar
        :ok="okRatio * 100"
        :failed="failedRatio * 100"
      />
    </td>
  </tr>
</template>

<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import { useFormatters } from "@/composables/useFormatters";
import ProgressBar from "./ProgressBar.vue";

const { formatPercentage } = useFormatters();

const props = defineProps(["check", "name"]);
const router = useRouter();
const store = useStore();

const okRatio = computed(() => props.check.passed_count / props.check.total_count);
const failedRatio = computed(() => props.check.failed_count / props.check.total_count);
const naRatio = computed(() => props.check.undefined_count / props.check.total_count);

function detail() {
    router.push({
        name: "resourceCheckDetail",
        params: {
            check: props.name,
            datasetId: store.getters.datasetId,
        },
    });
}
</script>

<style scoped lang="scss">
@import "@/scss/variables";

td.check_name {
    padding-left: 35px;
}

.progress_column {
    padding-left: 40px;
}

.opacity {
    opacity: 0.6;
}
</style>
