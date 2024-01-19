export default {
  methods: {
    sort: function (checks, comparator, asc = true) {
      if (checks != null) {
        checks.sort(comparator);
        if (!asc) {
          checks.reverse();
        }
      }
    },
    compareNumbers: function (a, b) {
      return a - b;
    },
  },
};
