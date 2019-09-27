export default {
    data: function() {
        return {
            search: null,
            submitTimeout: null
        };
    },  
    watch: {
        search: function(value) {
            if (this.submitTimeout) {
                clearTimeout(this.submitTimeout)
            }
              
            this.submitTimeout = setTimeout(() => this.searchSetter(), this.submitTimeLimit)
        }
    },
    computed: {
        submitTimeLimit: function() {
            return 400
        }
    },
    mounted: function() {
        this.search = this.searchGetter()
    }
};