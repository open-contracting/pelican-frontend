<template>
    <div id="sidebar" class="col-1 col-sm-2 col-md-3 col-lg-3 col-xl-2 text-center">
        <p>
            <img src="@/assets/ocp_logo.png" />
        </p>
        <b-nav class="main_nav text-left">
            <b-nav-item class="nav-item" to="/">
                <span class="menu_icon_small">
                    <font-awesome-icon icon="cogs" />
                </span>
                {{ $t("sections.home").toUpperCase() }}
            </b-nav-item>

            <b-nav-item class="nav-item" to="/overview">
                <span class="menu_icon_small">
                    <font-awesome-icon icon="home" />
                </span>
                {{ $t("sections.overview").toUpperCase() }}
            </b-nav-item>

            <!-- <li class="nav-item">
                <a class="nav-link active" href="#">
                    <router-link to="/field">
                        <span class="menu_icon_small">
                            <font-awesome-icon icon="sliders-h" />
                        </span>
                        {{ $t("sections.field").toUpperCase() }}
                    </router-link>
                </a>
            </li>-->

            <b-nav-item class="nav-item" to="/resource" :disabled="!resourceLoaded">
                <span v-if="resourceLoaded" class="menu_icon_small">
                    <font-awesome-icon icon="list-alt" />
                </span>
                <span v-else class="menu_icon_spinner">
                    <b-spinner variant="default" small type="grow" class="spinner"></b-spinner>
                </span>
                {{ $t("sections.resource").toUpperCase() }}
            </b-nav-item>

            <b-nav-item class="nav-item" to="/dataset" :disabled="!datasetLoaded">
                <router-link to="/dataset">
                    <span v-if="datasetLoaded" class="menu_icon_small">
                        <font-awesome-icon icon="tasks" />
                    </span>
                    <span v-else class="menu_icon_spinner">
                        <b-spinner variant="default" small type="grow" class="spinner"></b-spinner>
                    </span>
                    {{ $t("sections.dataset").toUpperCase() }}
                </router-link>
            </b-nav-item>

            <!-- <li class="nav-item">
                <a class="nav-link active" href="#">
                    <router-link to="/time">
                        <span class="menu_icon_small">
                            <font-awesome-icon icon="history" />
                        </span>
                        {{ $t("sections.time").toUpperCase() }}
                    </router-link>
                </a>
            </li>-->
        </b-nav>
    </div>
</template>

<script>
import stateMixin from "@/plugins/stateMixins.js";

export default {
    mixins: [stateMixin],
    data: function() {
        return {};
    }
};
</script>


<style lang="scss">
@import "src/scss/main";

.main_nav {
    margin-top: 50px;
    display: inline-block;
}

.main_nav > li {
    display: block;
    margin-top: 10px;
    font-size: 0.8em;
}

.main_nav a {
    color: $menu_gray;
    font-weight: 500;
    letter-spacing: 0.05rem;
}

.main_nav a :hover {
    text-decoration: none;
}

.main_nav .menu_icon_small {
    font-size: 1.2rem;
    margin-right: 10px;
    position: relative;
    top: 2px;
    width: 25px;
    display: inline-block;
}

.main_nav .menu_icon_spinner {
    font-size: 1.2rem;
    margin-right: 10px;
    position: relative;
    top: -4px;
    left: 2px;
    width: 25px;
    display: inline-block;
}

#sidebar {
    background-color: white;
    padding-top: 50px;
    padding-left: 30px;
}
</style>