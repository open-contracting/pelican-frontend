<template>
  <tr
    class="clickable"
    @click="showChecks = !showChecks"
  >
    <!-- The split does not line up with the columns below lg, so the row spans them. -->
    <td colspan="5">
      <div class="row">
        <div class="col-4 col-lg-5 category">
          <div class="switcher text-center">
            <span v-if="resourceLevelStats.length > 0">
              <FontAwesomeIcon
                v-if="!showChecks"
                icon="chevron-right"
              />
              <FontAwesomeIcon
                v-if="showChecks"
                icon="chevron-down"
              />
            </span>
          </div>
          {{ $t("resourceLevel." + section + ".categoryName") }}
        </div>
        <div class="col-8 col-lg-7 text-end text-lg-start info_message">
          {{ $t("resourceLevel.averageScore.description", { applicable: applicableChecks, total: resourceLevelStats.length, average_score: formattedAvgScore }) }}
          <Tooltip :text="$t('resourceLevel.averageScore.tooltip')" />
        </div>
      </div>
    </td>
  </tr>
  <template v-if="showChecks">
    <ResourceLevelRow
      v-for="(value, name, index) in resourceLevelStats"
      :key="name"
      :check="value"
      :name="value.name"
      :index="index"
    />
  </template>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { useStore } from "vuex";
import { useFormatters } from "@/composables/useFormatters";
import { RESOURCE_CHECK_ORDER } from "@/config.js";
import { useUiStore } from "@/stores/ui.js";
import ResourceLevelRow from "./ResourceLevelRow.vue";
import Tooltip from "./Tooltip.vue";

const props = defineProps(["section", "filter"]);

const store = useStore();
const ui = useUiStore();
const { t } = useI18n();
const { formatPercentage } = useFormatters();

const showChecks = ref(false);

const resourceLevelStats = computed(() => {
  const result = store.getters.resourceLevelStatsBySection(props.section);

  return result
    .sort((a, b) => {
      const nameA = a.name;
      const nameB = b.name;
      if (RESOURCE_CHECK_ORDER.indexOf(nameA) < 0 && RESOURCE_CHECK_ORDER.indexOf(nameB) < 0) {
        if (nameA < nameB) {
          return -1;
        }

        return 1;
      }
      if (RESOURCE_CHECK_ORDER.indexOf(nameA) < 0) {
        return 1;
      }
      if (RESOURCE_CHECK_ORDER.indexOf(nameB) < 0) {
        return -1;
      }

      return RESOURCE_CHECK_ORDER.indexOf(nameA) - RESOURCE_CHECK_ORDER.indexOf(nameB);
    })
    .filter(props.filter);
});

const applicableChecks = computed(() => {
  let applicableCount = 0;
  for (const check of resourceLevelStats.value) {
    if (check.undefined_count < check.total_count) {
      applicableCount += 1;
    }
  }
  return applicableCount;
});

const formattedAvgScore = computed(() => {
  let passedCount = 0;
  let failedCount = 0;
  for (const check of resourceLevelStats.value) {
    passedCount += check.passed_count;
    failedCount += check.failed_count;
  }

  if (passedCount + failedCount === 0) {
    return t("resourceLevel.averageScore.undefined");
  }

  return formatPercentage(passedCount / (passedCount + failedCount));
});

watch(showChecks, (newShowChecks) => {
  if (newShowChecks) {
    ui.expandResourceCheck(props.section);
  } else {
    ui.collapseResourceCheck(props.section);
  }
});

onMounted(() => {
  showChecks.value = ui.isResourceCheckExpanded(props.section);
});
</script>

<style scoped lang="scss">
@import "@/scss/variables";

.info_message {
    color: $na_color;
    font-weight: 300;
}

.switcher {
    display: inline-block;
    font-size: 80%;
    width: 30px;
    color: $primary;
}

.category {
    font-weight: 700;
}
</style>
