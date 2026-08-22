<template>
  <span class="just_holder">
    <Loader v-if="isSubmitting" />
    <span v-if="result != null">
      <span v-if="result.status == 'ok' && !failedTags">
        <BAlert
          class="submit-result"
          variant="success"
          :model-value="true"
        >
          <span>
            {{ $t("datasetReport.status.ok") }}
          </span>
        </BAlert>
        <span class="info_prefix margin_bottom">{{ $t("datasetReport.link") }}:</span>
        <GoogleDocsLink :document-id="result.data.file_id" />
        <RetryOrCloseButtons
          variant="success"
          @retry="retry"
          @close="$emit('close')"
        />
      </span>
      <span v-if="result.status == 'ok' && failedTags">
        <BAlert
          class="submit-result"
          variant="warning"
          :model-value="true"
        >
          <span>
            {{ $t("datasetReport.status.warning") }}
          </span>
        </BAlert>

        <div class="margin_bottom">
          <span class="info_prefix">{{ $t("datasetReport.link") }}:</span>
          <GoogleDocsLink :document-id="result.data.file_id" />
        </div>
      </span>
      <span v-if="result.status == 'template_error'">
        <BAlert
          class="submit-result"
          variant="danger"
          :model-value="true"
        >
          <span>{{ $t("datasetReport.status.templateError") }}</span>
        </BAlert>
        <div class="info_prefix">{{ $t("datasetReport.errorReport") }}:</div>
        <div
          v-for="(error, index) in result.data"
          :key="index"
        >
          <div><span class="info_prefix">{{ $t("datasetReport.reason") }}:</span> {{ error.reason }}</div>
          <div><span class="info_prefix">{{ $t("datasetReport.fullTag") }}:</span> {{ error.full_tag }}</div>
          <div>
            <span class="info_prefix">{{ $t("datasetReport.link") }}:</span>
            <GoogleDocsLink :document-id="error.template_id" />
          </div>
        </div>
        <RetryOrCloseButtons
          variant="danger"
          @retry="retry"
          @close="$emit('close')"
        />
      </span>
      <span v-if="result.status == 'report_error'">
        <BAlert
          class="submit-result"
          variant="danger"
          :model-value="true"
        >
          <span>{{ $t("datasetReport.status.reportError") }}</span>
        </BAlert>

        <span class="info_prefix">{{ $t("datasetReport.reason") }}:</span> {{ result.data.reason }}
        <RetryOrCloseButtons
          variant="danger"
          @retry="retry"
          @close="$emit('close')"
        />
      </span>
      <span v-if="result.status == 'server_error'">
        <BAlert
          class="submit-result"
          variant="danger"
          :model-value="true"
        >
          <BRow>
            <BCol class="width">
              {{ $t("datasetReport.status.serverError") }}<br>
              {{ result.message }}
            </BCol>
          </BRow>
        </BAlert>
        <RetryOrCloseButtons
          variant="danger"
          @retry="retry"
          @close="$emit('close')"
        />
      </span>
      <span v-if="failedTags != null">
        <span class="info_prefix">{{ $t("datasetReport.warningList") }}:</span>
        <ul>
          <li
            v-for="(tag, index) in failedTags"
            :key="index"
          >
            {{ tag }}
          </li>
        </ul>
        <span class="info_prefix margin_bottom">{{ $t("datasetReport.warningEnd") }}</span>
        <RetryOrCloseButtons
          variant="warning"
          @retry="retry"
          @close="$emit('close')"
        />
      </span>
    </span>
    <form
      v-if="!isSubmitting && result == null"
      class="modal_box align-items-center"
    >
      <div class="row mb-3 section_row">
        <label
          class="col-3 col-form-label"
        ><div
          id="label-padding"
          class="label-padding"
        >
          {{ $t("datasetReport.reportLanguage") }}
        </div></label>
        <div class="col-9 top-margin">
          <BRow>
            <BCol
              v-for="(name, code) in LOCALES"
              :key="code"
              class="col-6"
            >
              <BFormRadio
                v-model="reportLanguage"
                :value="code"
                @update:model-value="setDocumentId"
              >
                <div class="top-margin">
                  {{ name }}
                </div>
              </BFormRadio>
            </BCol>
          </BRow>
          <BRow>
            <BCol class="col-12">
              <div class="form-text text-body-secondary">
                <p>{{ $t("datasetReport.reportLanguageTooltip") }}</p>
              </div>
            </BCol>
          </BRow>
        </div>
      </div>
      <div class="row mb-3 section_row">
        <label
          class="col-3 col-form-label"
        ><div class="label-padding">{{ $t("datasetReport.documentId") }}</div></label>
        <div class="col-9">
          <BFormInput
            id="documentIdInput"
            v-model="documentId"
            spellcheck="false"
            autocomplete="off"
            class="base_input"
            lazy-formatter
            :formatter="fileIdFormatter"
          />
          <div class="form-text text-body-secondary">
            <p>{{ $t("datasetReport.documentIdTooltip") }}</p>
            <p>{{ $t("datasetReport.documentIdPermissions", {user: settingsStore.settings.user}) }}</p>
          </div>
        </div>
      </div>
      <div class="row mb-3 section_row">
        <label
          class="col-3 col-form-label"
        ><div class="label-padding">{{ $t("datasetReport.folderId") }}</div></label>
        <div class="col-9">
          <BFormInput
            id="folderIdInput"
            v-model="folderId"
            spellcheck="false"
            autocomplete="off"
            class="base_input"
            lazy-formatter
            :formatter="fileIdFormatter"
          />
          <div class="form-text text-body-secondary">
            <p>{{ $t("datasetReport.folderIdTooltip") }}</p>
            <p>{{ $t("datasetReport.folderIdPermissions", {user: settingsStore.settings.user}) }}</p>
          </div>
        </div>
      </div>
      <div class="row mb-3 section_row">
        <label
          class="col-3 col-form-label"
        ><div class="label-padding">{{ $t("datasetReport.reportName") }}</div></label>
        <div class="col-9">
          <BFormInput
            id="reportNameInput"
            v-model="reportName"
            spellcheck="false"
            autocomplete="off"
            class="base_input"
          />
          <div class="form-text text-body-secondary">
            <p>{{ $t("datasetReport.reportNameTooltip") }}</p>
          </div>
        </div>
      </div>
      <div class="text-center">
        <button
          type="button"
          class="btn btn-primary submit_button"
          :disabled="dataset == null || !documentId || !folderId"
          @click="createDatasetReport"
        >
          {{ $t("datasetReport.submit") }}
        </button>
      </div>
    </form>
  </span>
</template>

<script setup lang="ts">
import { BAlert, BCol, BFormInput, BFormRadio, BRow } from "bootstrap-vue-next";
import { computed, ref } from "vue";
import api from "@/api.js";
import { useLocale } from "@/composables/useLocale";
import { CONFIG, LOCALES } from "@/config.js";
import { useSettingsStore } from "@/stores/settings.js";
import type { Dataset, GenerateReport, GenerateReportResponse } from "@/types.js";
import GoogleDocsLink from "./GoogleDocsLink.vue";
import Loader from "./Loader.vue";
import RetryOrCloseButtons from "./RetryOrCloseButtons.vue";

/** The response, or the failure that prevented one. */
type ReportResult = GenerateReportResponse | { status: "server_error"; message: string };

const props = defineProps<{
  dataset: Dataset | null;
}>();
defineEmits<{ close: [] }>();

const settingsStore = useSettingsStore();
const { locale } = useLocale();

const isSubmitting = ref(false);
// The export defaults to the user's language, which the user can still override here.
const reportLanguage = ref(locale.value);
const documentId = ref(settingsStore.settings.template[reportLanguage.value]);
const folderId = ref(settingsStore.settings.folder);
const reportName = ref("");
const result = ref<ReportResult | null>(null);

// A report and a template error both list the tags that could not be rendered.
const failedTags = computed(() => {
  const tags = result.value != null && "failed_tags" in result.value ? result.value.failed_tags : [];
  return tags.length ? tags : null;
});

// The radio's value is the selected language, which its model types loosely.
function setDocumentId(value: unknown) {
  if (typeof value !== "string") {
    return;
  }

  // Only change the template if it is one of the default values.
  if (Object.values(settingsStore.settings.template).includes(documentId.value)) {
    documentId.value = settingsStore.settings.template[value];
  }
}

function createDatasetReport() {
  if (props.dataset == null) {
    return;
  }
  isSubmitting.value = true;

  const data: GenerateReport = {
    dataset_id: props.dataset.id,
    document_id: documentId.value,
    folder_id: folderId.value,
    language: reportLanguage.value,
  };
  if (reportName.value.trim() !== "") {
    data.report_name = reportName.value.trim();
  }

  api
    .postJSON<GenerateReportResponse>(`${CONFIG.apiBaseUrl}${CONFIG.apiEndpoints.createDatasetReport}`, data)
    .then((response) => {
      if (!response.ok) {
        result.value = { status: "server_error", message: response.statusText };
        return;
      }

      // The endpoint returns 200 even when the export fails, reporting it in the body's status property.
      result.value = response.data;
    })
    .catch((error: unknown) => {
      result.value = { status: "server_error", message: error instanceof Error ? error.message : String(error) };
    })
    .finally(() => {
      isSubmitting.value = false;
    });
}

function retry() {
  result.value = null;
  createDatasetReport();
}

function fileIdFormatter(value: string) {
  let valueMatch = value.match(/\/d\/([^/]+)/);
  if (valueMatch == null) {
    valueMatch = value.match(/\/folders\/([^/]+)/);
  }
  return valueMatch != null ? valueMatch[1] : value;
}
</script>

<style scoped lang="scss">
.submit-result {
    display: flex;
    justify-content: space-between;
}

.margin_bottom {
    margin-bottom: 1em;
}

.base_input {
    font-family: $font-family-mono;
}

.info_prefix {
    color: $headings-light-color;
}

.width {
    width: 100%;
}

.top-margin {
    padding-top: 0.25rem;
}

.label-padding {
    padding-top: 0.25em;
}
</style>
