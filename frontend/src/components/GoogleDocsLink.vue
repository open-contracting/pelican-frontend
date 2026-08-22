<template>
  <a
    v-if="url"
    :href="url"
    target="_blank"
  >{{ url }}</a>
</template>

<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{
  documentId: string | null;
}>();

// A template error names no document if it failed before reaching one.
const url = computed(() => (props.documentId ? `https://docs.google.com/document/d/${props.documentId}` : null));
</script>
