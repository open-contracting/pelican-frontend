<template>
    <div class="resource_level_check_detail">
        <h3>{{ $t("header").toUpperCase() }}</h3>
        <h2>{{ $t("resourceLevel." + check.name + ".name") }}</h2>
        <p>{{ $t("resourceLevel." + check.name + ".description") }}</p>
        <h5>{{$t("resourceLevel.count.header")}} {{ check.ok + check.failed + check.na | formatNumber }}</h5>
        <div class="result_box">
            <table class="table table-borderless">
                <tbody>
                    <tr class="d-flex">
                        <td class="col-2">
                            <span class="check_name">{{ $t("passed") }}</span>
                        </td>
                        <td class="col-1 text-right">{{ check.ok | formatNumber }}</td>
                    </tr>
                    <tr class="d-flex">
                        <td class="col-2">
                            <span class="check_name">{{ $t("failed") }}</span>
                        </td>
                        <td class="col-1 text-right">{{ check.failed | formatNumber }}</td>
                    </tr>
                    <tr class="d-flex">
                        <td class="col-2">
                            <span class="check_name">{{ $t("notAvailable") }}</span>
                        </td>
                        <td class="col-1 text-right">{{ check.na | formatNumber }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
export default {
    name: "resourceCheckDetail",
    data: function() {
        return {
            check: null
        };
    },
    components: {},
    created() {
        this.check = this.$store.getters.resourceLevelCheckByName(
            this.$route.params.check
        );
    },
    methods: {
        onePercent: function() {
            return (this.check.ok + this.check.failed + this.check.na) / 100;
        }
    },
    computed: {
        okPercentage() {
            return Math.round(this.check.ok / this.onePercent());
        },
        failedPercentage() {
            return Math.round(this.check.failed / this.onePercent());
        },
        naPercentage() {
            return Math.round(this.check.na / this.onePercent());
        }
    }
};
</script>
