<template>
    <plain>
        <h2>{{ $t("sections.home") }}</h2>
        <div class="result_box">
            <DatasetPicker />
        </div>
    </plain>
</template>

<script>
import DatasetPicker from "@/components/DatasetPicker.vue";
import Plain from "@/views/layouts/Plain.vue";

export default {
    name: "home",
    components: {
        DatasetPicker,
        Plain
    }
};
</script>

