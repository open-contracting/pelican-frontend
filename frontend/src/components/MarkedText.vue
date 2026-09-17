<!-- The app preserves template whitespace, so the segments share a line: a break between them would render. -->
<template>
  <template v-for="(segment, index) in segments" :key="index"><mark v-if="segment.matched">{{ segment.text }}</mark><template v-else>{{ segment.text }}</template></template>
</template>

<script setup lang="ts">
import type { PathSegment } from "@/composables/useFieldCheckSearch.js";

defineProps<{
  segments: PathSegment[];
}>();
</script>
