<template>
  <div
    class="tr row clickable align-items-center"
    @click="detail()"
  >
    <div class="col-9 col-lg-5 break_word check_name">
      <span>{{ $t("resourceLevel." + name + ".name") }}</span>
    </div>
    <div class="td col-1 col-lg-1 text-end">
      <span
        v-if="okRatio"
        class="value_ok"
      >{{ $filters.formatPercentage(okRatio) }}</span>
      <span
        v-else
        class="value_na opacity"
      >{{ $filters.formatPercentage(okRatio) }}</span>
    </div>
    <div class="td col-1 col-lg-1 text-end">
      <span
        v-if="failedRatio"
        class="value_failed"
      >{{ $filters.formatPercentage(failedRatio) }}</span>
      <span
        v-else
        class="value_na opacity"
      >{{ $filters.formatPercentage(failedRatio) }}</span>
    </div>
    <div class="td col-1 col-lg-1 text-end">
      <span
        v-if="naRatio"
        class="value_na"
      >{{ $filters.formatPercentage(naRatio) }}</span>
      <span
        v-else
        class="value_na opacity"
      >{{ $filters.formatPercentage(naRatio) }}</span>
    </div>
    <div class="td col-4 d-none d-lg-block progress_column">
      <ProgressBar
        :ok="okRatio * 100"
        :failed="failedRatio * 100"
      />
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import ProgressBar from "./ProgressBar.vue";

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

.check_name {
    padding-left: 65px;
}

.progress_column {
    padding-left: 40px;
}

.opacity {
    opacity: 0.6;
}
</style>
