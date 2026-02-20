<template>
  <div class="result_box loader text-center">
    <div class="spinner">
      <BSpinner
        variant="primary"
        style="width: 4rem; height: 4rem"
        type="grow"
        class="spinner"
      />
    </div>
    {{ $t("loader.generic") }}
  </div>
</template>

<script>
import { BSpinner } from "bootstrap-vue-next";

export default {
    components: { BSpinner },
    data: () => ({}),
};
</script>

<style scoped lang="scss">
.loader {
    font-size: 19px;
    font-weight: 700;
    padding: 40px;
}

.spinner {
    margin-bottom: 40px;
    font-size: 40px;
}
</style>
