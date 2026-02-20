<template>
  <BApp>
    <div
      id="app"
      class="container-fluid"
    >
      <router-view />
    </div>
  </BApp>
</template>

<script>
import { BApp } from "bootstrap-vue-next";

export default {
    components: { BApp },
    data: () => ({}),
};
</script>
