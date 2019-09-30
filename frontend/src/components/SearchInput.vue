<template>
    <b-input-group class="search_input">
        <template v-slot:prepend>
            <b-input-group-text>
                <font-awesome-icon icon="search"/>
            </b-input-group-text>
        </template>
        <b-form-input v-model="search" :placeholder="placeholder" />
    </b-input-group>
</template>

<script>

export default {
    data: function() {
        return {
            search: null,
            submitTimeout: null
        };
    },
    props: {
        placeholder: String,
        onUpdate: Function,
        preset: String,
        submitTimeLimit: {type: Number, default: 400}
    },
    watch: {
        search: function(value) {
            if (this.submitTimeout) {
                clearTimeout(this.submitTimeout)
            }
              
            this.submitTimeout = setTimeout(() => this.onUpdate(value), this.submitTimeLimit)
        }
    },
    mounted: function() {
        this.search = this.preset
    }
};
</script>

<style scoped lang="scss">
@import "src/scss/main";

.search_input {
    .input-group-text {
        background-color: transparent;
        border-right: none;
    }
    input {
        background-color: transparent;
        border-left: none;
    }
}
</style>