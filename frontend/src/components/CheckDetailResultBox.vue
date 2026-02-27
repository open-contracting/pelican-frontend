<template>
  <div class="result_box" :class="classes">
    <table class="table table-borderless table-sm">
      <tbody>
        <tr
          v-if="ok && 'passed_count' in check"
          class="d-flex"
        >
          <td class="col-3 text-end label">
            {{ $t(passedLabel) }}
          </td>
          <td class="col-9 align-middle">
            <InlineBar
              :numerator="check.passed_count"
              :denominator="check.total_count"
              :count="check.passed_count"
              state="ok"
              :show-count="true"
            />
          </td>
        </tr>
        <tr
          v-if="failed && 'failed_count' in check"
          class="d-flex"
        >
          <td class="col-3 text-end label">
            {{ $t(failedLabel) }}
          </td>
          <td class="col-9 align-middle">
            <InlineBar
              :numerator="check.failed_count"
              :denominator="check.total_count"
              :count="check.failed_count"
              state="failed"
              :show-count="true"
            />
          </td>
        </tr>
        <tr
          v-if="na && 'undefined_count' in check"
          class="d-flex"
        >
          <td class="col-3 text-end label">
            {{ $t("notAvailable") }}
          </td>
          <td class="col-9 align-middle">
            <InlineBar
              :numerator="check.undefined_count"
              :denominator="check.total_count"
              :count="check.undefined_count"
              state="na"
              :show-count="true"
            />
          </td>
        </tr>
        <tr
          v-if="individualPass && 'individual_passed_count' in check"
          class="d-flex"
        >
          <td class="col-3 text-end label">
            {{ $t("passed") }}
          </td>
          <td class="col-9 align-middle">
            <InlineBar
              :numerator="check.individual_passed_count"
              :denominator="check.individual_application_count"
              :count="check.individual_passed_count"
              state="ok"
              :show-count="true"
            />
          </td>
        </tr>
        <tr
          v-if="individualNonPass && 'individual_failed_count' in check"
          class="d-flex"
        >
          <td class="col-3 text-end label">
            {{ $t("failed") }}
          </td>
          <td class="col-9 align-middle">
            <InlineBar
              :numerator="check.individual_failed_count"
              :denominator="check.individual_application_count"
              :count="check.individual_failed_count"
              state="failed"
              :show-count="true"
            />
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import InlineBar from "./InlineBar.vue";

defineProps({
    check: Object,
    ok: Boolean,
    failed: Boolean,
    na: Boolean,
    individualPass: Boolean,
    individualNonPass: Boolean,
    passedLabel: {
        type: String,
        default: "passed",
    },
    failedLabel: {
        type: String,
        default: "failed",
    },
    classes: String,
});
</script>

<style scoped lang="scss">
.table td.label {
    padding-top: 8px;
}
</style>
