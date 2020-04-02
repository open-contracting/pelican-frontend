<template>
    <vue-context ref="menu">
        <li>
            <a class="clickable" @click.prevent="openNewTab">
                {{ $t("navigationContextMenu.openNewTab") }}
            </a>
        </li>
        <li>
            <a class="clickable" v-on:click="openNewWindow">
                {{ $t("navigationContextMenu.openNewWindow") }}
            </a>
        </li>
    </vue-context>
</template>

<script>
import VueContext from 'vue-context';
import 'vue-context/src/sass/vue-context.scss';


export default {
    data: function() {
        return {
            routerArguments: null
        };
    },
    name: "navigation-context-menu",
    components: { VueContext },
    methods: {
        openNewTab: function() {
            var routeData = this.$router.resolve(this.routerArguments);
            window.open(routeData.href);
        },
        openNewWindow: function() {
            var routeData = this.$router.resolve(this.routerArguments);
            window.open(routeData.href, '_blank', 'width=500,height=500,toolbar=yes,scrollbars=yes,resizable=yes');
        }
    },
    mounted() {
        this.$root.$on("navigationContextMenu", data => {
            this.$refs.menu.open(data.event);
            this.routerArguments = data.routerArguments;
        });
    },
    beforeDestroy() {
        this.$root.$off("navigationContextMenu", () => {});
    }
};
</script>
