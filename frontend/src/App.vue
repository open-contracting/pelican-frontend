<template>
    <div class="container-fluid" id="app">
        <router-view />
        <NavigationContextMenu/>
    </div>
</template>

<script>
import NavigationContextMenu from "@/components/NavigationContextMenu.vue";

export default {
    components: { NavigationContextMenu },
    data: function() {
        return {};
    }
};
</script>