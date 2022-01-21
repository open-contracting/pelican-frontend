<template>
  <vue-context ref="menu">
    <li>
      <a
        class="clickable"
        @click="openNewTab"
      >
        {{ $t("navigationContextMenu.openNewTab") }}
      </a>
    </li>
    <li>
      <a
        class="clickable"
        @click="openNewWindow"
      >
        {{ $t("navigationContextMenu.openNewWindow") }}
      </a>
    </li>
    <li>
      <a
        class="clickable"
        @click="copyToClipboard"
      >
        {{ $t("navigationContextMenu.copyToClipboard") }}
      </a>
    </li>
  </vue-context>
</template>

<script>
import VueContext from "vue-context";
import "vue-context/src/sass/vue-context.scss";

export default {
    name: "NavigationContextMenu",
    components: { VueContext },
    data: function () {
        return {
            routerData: null
        };
    },
    mounted() {
        this.$root.$on("navigationContextMenu", data => {
            this.$refs.menu.open(data.event);
            this.routerData = this.$router.resolve(data.routerArguments);
        });
    },
    beforeDestroy() {
        this.$root.$off("navigationContextMenu", () => {});
    },
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
    }
};
</script>
