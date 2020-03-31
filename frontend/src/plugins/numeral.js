import Vue from 'vue'

var numeral = require("numeral");

Vue.filter("formatNumber", function (value) {
    return numeral(value).format("0,0");
});

Vue.filter("formatNumber2D", function (value) {
    return numeral(value).format("0,0.00");
});

Vue.filter("formatPercentage", function (value) {
    var rounded = Math.round(value);

    if (rounded == 0.0 && value != 0.0) {
        return ">" + numeral(rounded).format("0") + "%";
    } else if (rounded == 100.0 && value != 100.0) {
        return "<" + numeral(rounded).format("0") + "%";
    } else {
        return numeral(rounded).format("0") + "%";
    }
});

Vue.filter("formatPercentage2D", function (value) {
    var rounded = Math.round(value * 100) / 100;

    if (rounded == 0.0 && value != 0.0) {
        return ">" + numeral(rounded).format("0.00") + "%";
    } else if (rounded == 100.0 && value != 100.0) {
        return "<" + numeral(rounded).format("0.00") + "%";
    } else {
        return numeral(rounded).format("0.00") + "%";
    }
});
