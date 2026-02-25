<template>
  <span class="just_holder">
    <Loader v-if="isSubmitting" />
    <span v-if="submitStatus != null">
      <span v-if="submitStatus == 'ok' && !failedTags">
        <BAlert
          class="submit-result"
          variant="success"
          :model-value="true"
        >
          <span>
            {{ $t("datasetReport.status.ok") }}
          </span>
        </BAlert>
        <span class="info_prefix margin_bottom">{{ $t("datasetReport.link") }}:&nbsp;</span>
        <a
          :href="'https://docs.google.com/document/d/' + submitData.file_id"
          target="_blank"
        >
          {{ "https://docs.google.com/document/d/" + submitData.file_id }}
        </a>
        <BRow class="buttons">
          <BCol>
            <button
              class="variant-success btn-success"
              href="#"
              @click.stop.prevent="retry"
            >
              <FontAwesomeIcon
                :icon="['fas', 'redo-alt']"
                class="icon"
              />
              {{ $t("tryAgain") }}
            </button>
          </BCol>
          <BCol class="right-align">
            <button
              class="variant-success btn-success"
              href="#"
              @click.stop.prevent="$emit('close')"
            >
              <FontAwesomeIcon
                :icon="['fas', 'window-close']"
                class="icon"
              />
              {{ $t("close") }}
            </button>
          </BCol>
        </BRow>
      </span>
      <span v-if="submitStatus == 'ok' && failedTags">
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
          <span class="info_prefix">{{ $t("datasetReport.link") }}:&nbsp;</span>
          <a
            :href="'https://docs.google.com/document/d/' + submitData.file_id"
            target="_blank"
          >
            {{ "https://docs.google.com/document/d/" + submitData.file_id }}&nbsp;
          </a>
        </div>
      </span>
      <span v-if="submitStatus == 'template_error'">
        <BAlert
          class="submit-result"
          variant="danger"
          :model-value="true"
        >
          <span>{{ $t("datasetReport.status.templateError") }}</span>
        </BAlert>
        <div class="info_prefix">{{ $t("datasetReport.errorReport") }}:</div>
        <div
          v-for="(error, index) in submitData"
          :key="index"
        >
          <div>reason: {{ error.reason }}</div>
          <div>full tag: {{ error.full_tag }}</div>
          <div>
            <span>link: </span>
            <a
              :href="'https://docs.google.com/document/d/' + error.template_id"
              target="_blank"
            >
              {{ "https://docs.google.com/document/d/" + error.template_id }}
            </a>
          </div>
        </div>
        <BRow class="buttons">
          <BCol>
            <button
              class="variant-danger btn-danger"
              href="#"
              @click.stop.prevent="retry"
            >
              <FontAwesomeIcon
                :icon="['fas', 'redo-alt']"
                class="icon"
              />
              {{ $t("tryAgain") }}
            </button>
          </BCol>
          <BCol class="right-align">
            <button
              class="variant-danger btn-danger"
              href="#"
              @click.stop.prevent="$emit('close')"
            >
              <FontAwesomeIcon
                :icon="['fas', 'window-close']"
                class="icon"
              />
              {{ $t("close") }}
            </button>
          </BCol>
        </BRow>
      </span>
      <span v-if="submitStatus == 'report_error'">
        <BAlert
          class="submit-result"
          variant="danger"
          :model-value="true"
        >
          <span>{{ $t("datasetReport.status.reportError") }}</span>
        </BAlert>

        <span class="info_prefix">{{ $t("datasetReport.reason") }}:&nbsp;</span>{{ submitData.reason }}
        <BRow class="buttons">
          <BCol>
            <button
              class="variant-danger btn-danger"
              href="#"
              @click.stop.prevent="retry"
            >
              <FontAwesomeIcon
                :icon="['fas', 'redo-alt']"
                class="icon"
              />
              {{ $t("tryAgain") }}
            </button>
          </BCol>
          <BCol class="right-align">
            <button
              class="variant-danger btn-danger"
              href="#"
              @click.stop.prevent="$emit('close')"
            >
              <FontAwesomeIcon
                :icon="['fas', 'window-close']"
                class="icon"
              />
              {{ $t("close") }}
            </button>
          </BCol>
        </BRow>
      </span>
      <span v-if="submitStatus == 'server_error'">
        <BAlert
          class="submit-result"
          variant="danger"
          :model-value="true"
        >
          <BRow>
            <BCol class="width">
              {{ $t("datasetReport.status.serverError") }}<br>
              {{ errorMessage }}
            </BCol>
          </BRow>
        </BAlert>
        <BRow>
          <BCol>
            <button
              class="variant-danger btn-danger"
              href="#"
              @click.stop.prevent="retry"
            >
              <FontAwesomeIcon
                :icon="['fas', 'redo-alt']"
                class="icon"
              />
              {{ $t("tryAgain") }}
            </button>
          </BCol>
          <BCol class="right-align">
            <button
              class="variant-danger btn-danger"
              href="#"
              @click.stop.prevent="$emit('close')"
            >
              <FontAwesomeIcon
                :icon="['fas', 'window-close']"
                class="icon"
              />
              {{ $t("close") }}
            </button>
          </BCol>
        </BRow>
      </span>
      <span v-if="failedTags != [] && failedTags != null">
        <span class="info_prefix">{{ $t("datasetReport.warningList") }}:&nbsp;</span>
        <ul>
          <li
            v-for="(tag, index) in failedTags"
            :key="index"
          >
            {{ tag }}
          </li>
        </ul>
        <span class="info_prefix margin_bottom">{{ $t("datasetReport.warningEnd") }}&nbsp;</span>
        <BRow class="buttons">
          <BCol>
            <button
              class="variant-warning btn-warning"
              href="#"
              @click.stop.prevent="retry"
            >
              <FontAwesomeIcon
                :icon="['fas', 'redo-alt']"
                class="icon"
              />
              {{ $t("tryAgain") }}
            </button>
          </BCol>
          <BCol class="right-align">
            <button
              class="variant-warning btn-warning"
              href="#"
              @click.stop.prevent="$emit('close')"
            >
              <FontAwesomeIcon
                :icon="['fas', 'window-close']"
                class="icon"
              />
              {{ $t("close") }}
            </button>
          </BCol>
        </BRow>
      </span>
    </span>
    <form
      v-if="!isSubmitting && submitStatus == null"
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
              v-for="option in options"
              :key="option.value"
              class="col-6"
            >
              <BFormRadio
                v-model="reportLanguage"
                :value="option.value"
                @change="setDocumentId"
              >
                <div class="top-margin">
                  {{ option.text }}
                </div>
              </BFormRadio>
            </BCol>
          </BRow>
          <BRow>
            <BCol class="col-12">
              <small
                class="form-text text-body-secondary"
                v-html="$t('datasetReport.reportLanguageTooltip')"
              />
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
          <small
            class="form-text text-body-secondary"
            v-html="$t('datasetReport.documentIdTooltip', {user: this.$store.getters.settings.user})"
          />
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
          <small
            class="form-text text-body-secondary"
            v-html="$t('datasetReport.folderIdTooltip', {user: this.$store.getters.settings.user})"
          />
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
          <small
            class="form-text text-body-secondary"
            v-html="$t('datasetReport.reportNameTooltip')"
          />
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

<script>
import axios from "axios";
import { BAlert, BCol, BFormInput, BFormRadio, BRow } from "bootstrap-vue-next";
import Loader from "@/components/Loader.vue";
import { CONFIG } from "@/config.js";

export default {
    components: { BAlert, BCol, BFormInput, BFormRadio, BRow, Loader },
    props: ["dataset"],
    emits: ["close"],
    data: function () {
        return {
            isSubmitting: false,
            documentId: this.$store.getters.settings.template.en,
            folderId: this.$store.getters.settings.folder,
            reportName: "",
            submitStatus: null,
            submitData: null,
            documentLink: null,
            errorMessage: null,
            failedTags: null,
            options: [
                { value: "en", text: "English" },
                { value: "es", text: "Español" },
            ],
            reportLanguage: "en",
        };
    },
    methods: {
        setDocumentId(value) {
            // Only change the template if it is one of the default values.
            if (Object.values(this.$store.getters.settings.template).includes(this.documentId)) {
                this.documentId = this.$store.getters.settings.template[value];
            }
        },
        createDatasetReport() {
            if (this.dataset == null) {
                return;
            }
            this.errorMessage = null;
            this.isSubmitting = true;

            const data = {
                dataset_id: Number.parseInt(this.dataset.id, 10),
                document_id: this.documentId,
                folder_id: this.folderId,
                language: this.reportLanguage,
            };
            if (this.reportName.trim() !== "") {
                data.report_name = this.reportName.trim();
            }

            axios
                .post(`${CONFIG.apiBaseUrl}${CONFIG.apiEndpoints.createDatasetReport}`, data)
                .then((response) => {
                    if (response.data.failed_tags && response.data.failed_tags.length === 0) {
                        this.failedTags = null;
                    } else {
                        this.failedTags = response.data.failed_tags;
                    }

                    if (response.status === 200) {
                        this.submitStatus = response.data.status;
                        this.submitData = response.data.data;
                    } else {
                        this.submitStatus = "server_error";
                        this.errorMessage = response.statusText;
                    }
                })
                .catch((error) => {
                    this.submitStatus = "server_error";
                    this.errorMessage = error;
                })
                .finally(() => {
                    this.isSubmitting = false;
                });
        },
        reset() {
            this.isSubmitting = false;
            this.documentId = "";
            this.folderId = "";
            this.reportName = "";
            this.submitStatus = null;
            this.submitData = null;
            this.documentLink = null;
            this.errorMessage = null;
        },
        retry() {
            this.submitStatus = null;
            this.createDatasetReport();
        },
        fileIdFormatter(value) {
            let valueMatch = value.match(/\/d\/([^/]+)/);
            if (valueMatch == null) {
                valueMatch = value.match(/\/folders\/([^/]+)/);
            }
            return valueMatch != null ? valueMatch[1] : value;
        },
    },
};
</script>

<style lang="scss">
@import "@/scss/main";

.submit-result {
    display: flex;
    justify-content: space-between;
}

.variant-success {
    color: #606602;
}

.variant-danger {
    color: #6c010e;
}

.modal_box {
    padding: 30px;
}

.modal_headline {
    padding-bottom: 30px;
}

.margin_bottom {
    margin-bottom: 1em;
}

.base_input,
.base_input:-internal-autofill-selected {
    width: 100%;
    height: 100%;
    padding-right: 0px;
    font-size: 13px;
    font-family: $font-family-mono;
    background-color: transparent;
}

.modal_input {
    font-weight: 400;
    line-height: 1.5;
    color: #212529;
}

.submit_button {
    font-size: 18px;
    font-weight: 700;
    color: $text-color;
    font-family: $font-family-sans-serif;
    background-color: transparent;
    border: 1px solid $na_color;
    margin-top: 20px;
}

.icon {
    margin-right: 0.5em;
}

.buttons {
    margin-top: 1em;
}

.right-align {
    text-align: right;
    align-items: flex-end;
}

.btn-danger,
.btn-warning,
.btn-success {
    border-radius: 5px;
    border: 1px solid $na_color;
    padding: 1em;
}

.submit_button:hover {
    background-color: $na_color;
    color: white;
    border: 1px solid $na_color;
}

.procuring_row {
    padding-top: 15px;
}

.section_row {
    padding-top: 30px;
}

.multiselect__tag-icon:after {
    content: "×";
    color: white;
    font-size: 16px;
}

.multiselect__tag-icon:focus,
.multiselect__tag-icon:hover {
    background: $gray-800;
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
