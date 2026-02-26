<template>
  <div
    id="sidebar"
    class="text-center"
  >
    <div class="row">
      <div
        id="sidebar_envelope"
        class="text-center"
      >
        <img
          id="logo"
          src="@/assets/ocp_logo.svg"
        >
        <BNav class="main_nav text-start">
          <BNavItem
            id="home_link"
            to="/"
          >
            <span class="menu_icon_small">
              <FontAwesomeIcon icon="cogs" fixed-width />
            </span>
            {{ $t("sections.home").toUpperCase() }}
          </BNavItem>

          <BNavItem
            :to="{ name: 'overview', params: { datasetId: datasetId } }"
          >
            <span class="menu_icon_small">
              <FontAwesomeIcon icon="home" fixed-width />
            </span>
            {{ $t("sections.overview").toUpperCase() }}
          </BNavItem>

          <BNavItem
            :to="{ name: 'field', params: { datasetId: datasetId } }"
            :disabled="!fieldLoaded"
          >
            <span
              v-if="fieldLoaded"
              class="menu_icon_small"
            >
              <FontAwesomeIcon icon="sliders-h" fixed-width />
            </span>
            <span
              v-else
              class="menu_icon_spinner"
            >
              <BSpinner
                small
                type="grow"
                class="spinner"
              />
            </span>
            {{ $t("sections.field").toUpperCase() }}
          </BNavItem>

          <BNavItem
            :to="{ name: 'resource', params: { datasetId: datasetId } }"
            :disabled="!resourceLoaded"
          >
            <span
              v-if="resourceLoaded"
              class="menu_icon_small"
            >
              <FontAwesomeIcon icon="list-alt" fixed-width />
            </span>
            <span
              v-else
              class="menu_icon_spinner"
            >
              <BSpinner
                small
                type="grow"
                class="spinner"
              />
            </span>
            {{ $t("sections.resource").toUpperCase() }}
          </BNavItem>

          <BNavItem
            :to="{ name: 'dataset', params: { datasetId: datasetId } }"
            :disabled="!datasetLoaded"
          >
            <span
              v-if="datasetLoaded"
              class="menu_icon_small"
            >
              <FontAwesomeIcon icon="tasks" fixed-width />
            </span>
            <span
              v-else
              class="menu_icon_spinner"
            >
              <BSpinner
                small
                type="grow"
                class="spinner"
              />
            </span>
            {{ $t("sections.dataset").toUpperCase() }}
          </BNavItem>

          <BNavItem
            v-if="showTimeVariance"
            :to="{ name: 'time', params: { datasetId: datasetId } }"
          >
            <span
              v-if="timeVarianceLoaded"
              class="menu_icon_small"
            >
              <FontAwesomeIcon icon="history" fixed-width />
            </span>
            <span
              v-else
              class="menu_icon_spinner"
            >
              <BSpinner
                small
                type="grow"
                class="spinner"
              />
            </span>
            {{ $t("sections.time").toUpperCase() }}
          </BNavItem>
        </BNav>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useStore } from "vuex";

const store = useStore();

const datasetId = computed(() => store.getters.datasetId);
const fieldLoaded = computed(() => store.getters.fieldLevelStats != null);
const resourceLoaded = computed(() => store.getters.resourceLevelStats != null);
const datasetLoaded = computed(() => store.getters.datasetLevelStats != null);
const timeVarianceLoaded = computed(() => store.getters.timeVarianceLevelStats != null);
const showTimeVariance = computed(
    () => store.getters.timeVarianceLevelStats != null && store.getters.timeVarianceLevelStats.length > 0,
);
</script>

<style lang="scss">
@import "@/scss/main";

#logo {
    width: 80%;
    max-width: 200px;
}

.main_nav {
    margin-top: 50px;
    display: inline-block;
}

.main_nav > li {
    display: block;
    margin-top: 10px;
    font-size: 0.8em;
    width: 100%;
}

.main_nav a {
    color: $menu_gray;
    font-weight: 500;
    letter-spacing: 0.05rem;
    text-decoration: none;
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
    position: relative;
    position: relative;
    width: 210px;
}

#sidebar_envelope {
    position: fixed;
    top: 0px;
    left: 0px;
    bottom: 0px;
    overflow-y: auto;
    padding: 50px 5px 30px 5px;
    width: 210px;
    background-color: white;
    z-index: 1000;
}

#sidebar_envelope .main_nav .nav-item .nav-link.active {
    color: $primary;
}

#sidebar_envelope .main_nav #home_link .nav-link {
    color: $menu_gray;
}

@media (max-width: 1199.99px) {
    #logo {
        width: 60px;
    }

    .main_nav > li {
        font-size: 0.6em;
    }

    #sidebar {
        position: relative;
        width: 70px;
    }

    #sidebar_envelope {
        background-color: white;
        position: fixed;
        width: 70px;
        top: 0px;
        left: 0px;
        bottom: 0px;
        overflow-y: auto;
        padding: 60px 0px 0px 0px;
        z-index: 100;
        border-right: 1px solid $na_light_color;
    }

    #sidebar_envelope .nav-item {
        text-align: center;
        margin-top: 0px;
    }

    #sidebar_envelope .main_nav a {
        color: $na_color;
    }

    #sidebar_envelope .nav-item :hover,
    #sidebar_envelope .main_nav .nav-item .nav-link.active:hover,
    #sidebar_envelope .main_nav #home_link .nav-link:hover {
        background-color: $na_color;
        color: white;
    }

    #sidebar_envelope .nav-link {
        padding: 0px;
        padding-top: 10px;
        padding-bottom: 10px;
    }

    #sidebar_envelope .main_nav .menu_icon_small {
        margin-right: 0px;
        display: block;
        margin: auto;
    }

    #sidebar_envelope .main_nav .menu_icon_small::after {
        content: "\A";
        white-space: pre;
    }
}
</style>
