export default {
    methods: {
        sort: (checks, comparator, asc = true) => {
            if (checks != null) {
                checks.sort(comparator);
                if (!asc) {
                    checks.reverse();
                }
            }
        },
        compareNumbers: (a, b) => a - b,
    },
};
