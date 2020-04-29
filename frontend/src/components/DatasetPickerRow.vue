<template>
    <div>
        <div
            @click="setDataset(dataset)"
            :class="['row','tr', 'clickable', 'align-items-center', {disabled: !isDatasetImported(dataset)}]"
            @contextmenu.prevent="$root.$emit('navigationContextMenu', {event: $event, routerArguments: {name: 'overview', params: {datasetId: dataset.id}}})"
        >
            <div
                v-if="depth != 0"
                :class="'td col-' + depth"
            />
            <div :class="'td col-' + (4 - depth)">
                <span v-if="dataset.filtered_children.length != 0" v-on:click.stop="showFilteredChildren = !showFilteredChildren">
                    <div v-if="!showFilteredChildren" class="switcher text-center">
                        <font-awesome-icon icon="chevron-right" />
                    </div>
                    <div v-if="showFilteredChildren" class="switcher text-center">
                        <font-awesome-icon icon="chevron-down" />
                    </div>
                </span>
                {{ dataset.name }}
                <span class="dataset_id">(Id {{ dataset.id }})</span>
            </div>
            <div class="td col-1 numeric text-right">{{ dataset.size | formatNumber }}</div>
            <div v-if="dataset.meta.kingfisher_metadata" class="td col-1 numeric text-right">{{ dataset.meta.kingfisher_metadata.collection_id }}</div>
            <div class="td col-1 phase_cell align-items-center align-middle">
                <template v-if="dataset.phase == 'CHECKED' && dataset.state == 'OK'">
                    <span class="small_icon">
                        <font-awesome-icon :icon="['far', 'check-circle']" class="text-success" />
                    </span>
                    {{ dataset.phase }}
                </template>
                <template v-else-if="dataset.state == 'FAILED'">
                    <span class="small_icon">
                        <font-awesome-icon :icon="['far', 'times-circle']" class="text-danger" />
                    </span>
                    {{ dataset.phase }}
                </template>
                <template v-else>
                    <b-row class="progress_label no-gutters">
                        <b-col v-for="p in phases" :key="p">
                            <template v-if="p == dataset.phase">{{ p }}</template>
                        </b-col>
                    </b-row>

                    <ProgressBar :value="getDatasetProgress(dataset)" />
                </template>
            </div>
            <div class="td col numeric">
                <span class="created">{{ dataset.created }}</span>
                <br />
                <span class="modified">{{ dataset.modified }}</span>
            </div>
            <div class="td col">
                <b-link
                    v-if="dataset.ancestor_id"
                    class="time_varinace break_word"
                    @click.stop="setDataset(dataset, {name: 'time'})"
                    :title="dataset.ancestor_id"
                >
                    <span class="small_icon">
                        <font-awesome-icon icon="history" />
                    </span>
                    dataset.ancestor_id
                </b-link>
            </div>
            <div class="td col">
                <a href="#">{{ $t("dataset.filter") }}</a>    
                <!-- <a v-on:click.stop.prevent="download(item.item_id)" href="#">{{ $t("examples.download_json") }}</a>     -->
            </div>
        </div>
        <template v-for="(item, index) in dataset.filtered_children">
            <DatasetPickerRow
                v-if="showFilteredChildren"
                v-bind:key="index"
                :dataset="item"
                :depth="depth + 1"
            />
        </template>
    </div>
</template>

<script>
import ProgressBar from "@/components/ProgressBar.vue";
import stateMixin from "@/plugins/stateMixins.js";
import sortMixins from "@/plugins/sortMixins.js";

export default {
    name: 'DatasetPickerRow',
    mixins: [stateMixin, sortMixins],
    data: function() {
        return {
            loading: false,
            afterUpdateRoute: { name: "overview" },
            showFilteredChildren: false,
        };
    },
    components: {ProgressBar,},
    props: ["dataset", "depth"],
    computed: {
        phases: function() {
            return [
                "PLANNED",
                "CONTRACTING_PROCESS",
                "DATASET",
                "TIME_VARIANCE",
                "CHECKED"
            ];
        },
    },
    methods: {
        setDataset: function(dataset, route = { name: "overview" }) {
            if (!this.isDatasetImported(dataset)) {
                return;
            }

            this.loading = true;
            this.afterUpdateRoute = route;
            this.afterUpdateRoute.params = { datasetId: dataset.id };
            if (this.$store.getters.datasetId != dataset.id) {
                this.$store.dispatch("updateDataset", dataset);
            } else {
                this.$router.push(this.afterUpdateRoute);
            }
        },
        getDatasetProgress: function(dataset) {
            return (this.phases.indexOf(dataset.phase) + 1) * 20;
        },
        isDatasetImported: function(dataset) {
            return dataset.phase == "CHECKED" && dataset.state == "OK";
        }
    },
    watch: {
        atLeastOneLoaded: function(newValue) {
            if (newValue) {
                this.$router.push(this.afterUpdateRoute);
            }
        }
    }
};
</script>

<style scoped lang="scss">
@import "src/scss/main";

.switcher {
    display: inline-block;
    font-size: 80%;
    width: 30px;
    color: $primary;
}

.form-control::placeholder {
    color: red;
}

.small_icon {
    position: relative;
    top: -1px;
}

.picker_table {
    padding: 30px;
}

.search_input {
    margin-bottom: 20px;
}

.tr {
    &.disabled {
        cursor: not-allowed;

        a {
            cursor: not-allowed;
            &:hover {
                text-decoration: none;
            }
        }
    }
}

.th {
    .modified {
        font-family: $font-family-thin;
        color: $headings_light_color;
    }
}

.td {
    .created {
        font-weight: 700;
    }

    .modified {
        color: $headings_light_color;
    }

    &:nth-of-type(4) {
        white-space: nowrap;
    }

    .dataset_id {
        color: $na_color;
        font-family: $font-family-thin;
        font-size: 14px;
    }
}

.phase_cell {
    font-family: $font-family-thin;

    .progress_label {
        font-size: 11px;

        .col {
            white-space: nowrap;
        }

        .state-failed {
            color: $failed_color;
        }
    }
}

.time_varinace {
    font-family: $font-family-thin;
    color: $primary;
    max-width: 110px;

    svg {
        margin-right: 4px;
    }
}

.action_bar {
    margin-top: 15px;
    margin-bottom: 15px;
}
</style>