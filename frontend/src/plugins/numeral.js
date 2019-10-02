import Vue from 'vue'

var numeral = require("numeral");

Vue.filter("formatNumber", function (value) {
    return numeral(value).format("0,0");
});

Vue.filter("formatNumber2D", function (value) {
    return numeral(value).format("0,0.00");
});