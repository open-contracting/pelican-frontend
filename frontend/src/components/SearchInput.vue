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

<script setup>
import { BButton, BFormInput, BInputGroup, BInputGroupText } from "bootstrap-vue-next";
import { onMounted, ref, watch } from "vue";

const props = defineProps({
  placeholder: String,
  preset: String,
});

const emit = defineEmits(["search"]);

const search = ref(null);
let submitTimeout = null;

watch(search, (value) => {
  if (submitTimeout) {
    clearTimeout(submitTimeout);
  }

  submitTimeout = setTimeout(() => emit("search", value), 400);
});

onMounted(() => {
  search.value = props.preset;
});
</script>

<style scoped lang="scss">

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
