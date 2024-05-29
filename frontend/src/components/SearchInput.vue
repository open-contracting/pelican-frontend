<template>
  <b-input-group class="search_input">
    <template #prepend>
      <b-input-group-text>
        <font-awesome-icon icon="search" />
      </b-input-group-text>
    </template>
    <b-form-input
      v-model="search"
      :placeholder="placeholder"
    />
    <template #append>
      <b-button
        v-if="search"
        :disabled="!search"
        @click="search = null"
      >
        <font-awesome-icon :icon="['fas', 'times']" />
      </b-button>
    </template>
  </b-input-group>
</template>

<script>
export default {
    props: {
        placeholder: String,
        onUpdate: Function,
        preset: String,
        submitTimeLimit: { type: Number, default: 400 },
    },
    data: function () {
        return {
            search: null,
            submitTimeout: null,
        };
    },
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
@import "src/scss/main";

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
