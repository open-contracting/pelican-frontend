<template>
    <span>
        <span v-for="section in examples" v-bind:key="section[0]">
            <h5>{{ section[0] }}</h5>
            <div class="result_box">
                <table class="table table-sm">
                    <thead>
                        <tr class="d-flex">
                            <th class="col-10" scope="col">{{ $t("examples.ocid") }}</th>
                            <th class="col-2 text-left" scope="col">{{ $t("examples.actions") }}</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(item, index) in section[1].slice(0, 5)" class="d-flex" v-bind:key="index">
                            <td class="col-10 text-left numeric">
                                <span class="check_name">{{ item.ocid }}</span>
                            </td>
                            <td class="col-2 clickable" v-on:click="changePreview(index, section[0], item)">
                                <span v-if="index != selectedKey || selectedSection != section[0]">{{ $t("examples.preview") }}</span>
                                <span class="badge badge-primary" v-if="index == selectedKey && selectedSection == section[0]">active</span>
                            </td>
                        </tr>
                        <tr v-if="!visibleSections(section[0])">
                            <td colspan="2" class="text-center bold clickable moreLess" v-on:click.stop="showMore(section[0])">
                                <a>
                                    <font-awesome-icon icon="chevron-down" />
                                    {{ $t("examples.showMore") }}
                                </a>
                            </td>
                        </tr>
                        <span v-if="visibleSections(section[0])">
                            <tr v-for="(item, index) in section[1].slice(5, )" class="d-flex" v-bind:key="index">
                                <td class="col-10 text-left numeric">
                                    <span class="check_name">{{ item.ocid }}</span>
                                </td>
                                <td class="col-2 clickable" v-on:click="changePreview(index + 5, section[0], item)">
                                    <span v-if="index + 5 != selectedKey || selectedSection != section[0]">{{ $t("examples.preview") }}</span>
                                    <span class="badge badge-primary" v-if="index + 5 == selectedKey && selectedSection == section[0]">active</span>
                                </td>
                            </tr>
                        </span>
                        <tr v-if="visibleSections(section[0])">
                            <td colspan="2" class="text-center bold clickable moreLess" v-on:click.stop="showLess(section[0])">
                                <a>
                                    <font-awesome-icon icon="chevron-up" />
                                    {{ $t("examples.showLess") }}
                                </a>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </span>
    </span>
</template>

<script>
export default {
    data: function() {
        return {
            openSections: [],
            selectedKey: null,
            selectedSection: null
        };
    },
    props: ["examples"],
    methods: {
        changePreview: function(key, section, item) {
            this.selectedKey = key;
            this.selectedSection = section;
            this.previewData = item;
        },
        showMore: function(section) {
            this.openSections.push(section);
        },
        showLess: function(section) {
            this.openSections = this.openSections.filter(function(item) {
                return item !== section;
            });
        },
        visibleSections: function(section) {
            return this.openSections.includes(section);
        }
    },
    computed: {}
};
</script>

<style scoped lang="scss">
@import "src/scss/variables";

.moreLess {
    padding-top: 25px;
}
</style>