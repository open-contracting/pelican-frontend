<template>
    <div class="container-fluid p-0" id="app">
        <div class="row h-100">
            <nav class="col-1 col-sm-2 col-md-3 col-lg-3 col-xl-2 sidebar h-100 text-center">
                <img src="./assets/ocp_logo.png" />
                <br />
                <ul class="nav main_nav text-left">
                    <li class="nav-item">
                        <a class="nav-link active" href="#">
                            <router-link to="/">
                                <span class="menu_icon_small">
                                    <font-awesome-icon icon="cogs" />
                                </span>
                                {{ $t("sections.home").toUpperCase() }}
                            </router-link>
                        </a>
                    </li>

                    <li class="nav-item">
                        <a class="nav-link active" href="#">
                            <router-link to="/">
                                <span class="menu_icon_small">
                                    <font-awesome-icon icon="home" />
                                </span>
                                {{ $t("sections.overview").toUpperCase() }}
                            </router-link>
                        </a>
                    </li>

                    <li class="nav-item">
                        <a class="nav-link active" href="#">
                            <router-link to="/field">
                                <span class="menu_icon_small">
                                    <font-awesome-icon icon="sliders-h" />
                                </span>
                                {{ $t("sections.field").toUpperCase() }}
                            </router-link>
                        </a>
                    </li>

                    <li class="nav-item">
                        <a class="nav-link active" href="#">
                            <router-link to="/resource">
                                <span class="menu_icon_small">
                                    <font-awesome-icon icon="list-alt" />
                                </span>
                                {{ $t("sections.resource").toUpperCase() }}
                            </router-link>
                        </a>
                    </li>

                    <li class="nav-item">
                        <a class="nav-link active" href="#">
                            <router-link to="/dataset">
                                <span class="menu_icon_small">
                                    <font-awesome-icon icon="tasks" />
                                </span>
                                {{ $t("sections.dataset").toUpperCase() }}
                            </router-link>
                        </a>
                    </li>

                    <li class="nav-item">
                        <a class="nav-link active" href="#">
                            <router-link to="/time">
                                <span class="menu_icon_small">
                                    <font-awesome-icon icon="history" />
                                </span>
                                {{ $t("sections.time").toUpperCase() }}
                            </router-link>
                        </a>
                    </li>
                </ul>
            </nav>

            <router-view />
        </div>
    </div>
</template>

<script>
export default {
    data: function() {
        return {
            datasetId: "honduras_2019-07-11_16:32:23"
        };
    },
    mounted() {
        this.$store.dispatch("updateDatasetId", "honduras_2019-07-11_16:32:23");
    }
};
</script>

<style lang="scss">
@import "src/scss/main";

.main_nav {
    margin-top: 50px;
    display: inline-block;
    position: relative;
    left: -10px;
}

.main_nav > li {
    display: block;
    width: 100%;
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
    padding-right: 10px;
    position: relative;
    top: 2px;
}
</style>
