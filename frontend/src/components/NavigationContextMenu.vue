<template>
    <vue-context ref="menu">
        <li>
            <a class="clickable" v-on:click="openNewTab">
                {{ $t("navigationContextMenu.openNewTab") }}
            </a>
        </li>
        <li>
            <a class="clickable" v-on:click="openNewWindow">
                {{ $t("navigationContextMenu.openNewWindow") }}
            </a>
        </li>
        <li>
            <a class="clickable" v-on:click="copyToClipboard">
                {{ $t("navigationContextMenu.copyToClipboard") }}
            </a>
        </li>
    </vue-context>
</template>

<script>
import VueContext from "vue-context";
import "vue-context/src/sass/vue-context.scss";

export default {
    data: function () {
        return {
            routerData: null
        };
    },
    name: "navigation-context-menu",
    components: { VueContext },
    methods: {
        openNewTab: function () {
            window.open(this.routerData.href);
        },
        openNewWindow: function () {
            window.open(
                this.routerData.href,
                "_blank",
                "width=500,height=500,toolbar=yes,scrollbars=yes,resizable=yes"
            );
        },
        copyToClipboard: function () {
            this.$clipboard(window.location.origin + this.routerData.href);
        }
    },
    mounted() {
        this.$root.$on("navigationContextMenu", data => {
            this.$refs.menu.open(data.event);
            this.routerData = this.$router.resolve(data.routerArguments);
        });
    },
    beforeDestroy() {
        this.$root.$off("navigationContextMenu", () => {});
    }
};
</script>
