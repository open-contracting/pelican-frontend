<template>
    <div id="app" class="container-fluid">
        <router-view />
        <NavigationContextMenu />
    </div>
</template>

<script>
import NavigationContextMenu from "@/components/NavigationContextMenu.vue";

export default {
    components: { NavigationContextMenu },
    data: function () {
        return {};
    }
};
</script>
