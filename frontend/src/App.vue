<template>
    <div class="container-fluid" id="app">
        <div class="row h-100">
            <nav class="col-md-2 d-none d-md-block sidebar h-100">
                <div class="sidebar-sticky text-center">
                    <img src="./assets/ocp_logo.png" />
                    <ul class="nav main_nav text-left">
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
                </div>
            </nav>

            <main role="main" class="col-md-9 ml-sm-auto col-lg-10 px-4">
                <div class="align-items-center">
                    <router-view />
                </div>
            </main>
        </div>
    </div>
</template>

<style lang="scss">
@import "src/scss/main";

.main_nav {
    margin-top: 30px;
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
