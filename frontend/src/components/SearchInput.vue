<template>
  <BInputGroup class="search_input">
    <template #prepend>
      <BInputGroupText>
        <FontAwesomeIcon icon="search" />
      </BInputGroupText>
    </template>
    <BFormInput
      v-model="search"
      :placeholder="placeholder"
    />
    <template #append>
      <BButton
        v-if="search"
        :disabled="!search"
        @click="search = null"
      >
        <FontAwesomeIcon :icon="['fas', 'times']" />
      </BButton>
    </template>
  </BInputGroup>
</template>

<script>
import { BButton, BFormInput, BInputGroup, BInputGroupText } from "bootstrap-vue-next";

export default {
    components: { BButton, BFormInput, BInputGroup, BInputGroupText },
    props: {
        placeholder: String,
        onUpdate: Function,
        preset: String,
        submitTimeLimit: { type: Number, default: 400 },
    },
    data: () => ({
        search: null,
        submitTimeout: null,
    }),
    watch: {
        search: function (value) {
            if (this.submitTimeout) {
                clearTimeout(this.submitTimeout);
            }

            this.submitTimeout = setTimeout(() => this.onUpdate(value), this.submitTimeLimit);
        },
    },
    mounted: function () {
        this.search = this.preset;
    },
};
</script>

<style scoped lang="scss">
@import "@/scss/main";

.search_input {
    .input-group-text {
        background-color: transparent;
        border-right: none;
    }
    input {
        background-color: transparent;
        border-left: none;
        padding-top: 10px;
    }
}
</style>
