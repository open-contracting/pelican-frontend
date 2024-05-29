import Vue from "vue";

const numeral = require("numeral");

Vue.filter("formatNumber", (value) => {
    if (value === undefined) {
        return value;
    }
    return numeral(value).format("0,0");
});

Vue.filter("formatNumber2D", (value) => numeral(value).format("0,0.00"));

Vue.filter("formatPercentage", (value) => {
    const rounded = Math.round(value);

    if (rounded === 0.0 && value !== 0.0) {
        return `>${numeral(rounded).format("0")}%`;
    }
    if (rounded === 100.0 && value !== 100.0) {
        return `<${numeral(rounded).format("0")}%`;
    }
    return `${numeral(rounded).format("0")}%`;
});

Vue.filter("formatPercentageOmitZero", (value) => {
    const rounded = Math.round(value);

    if (value === 0.0) {
        return "";
    }
    if (rounded === 0.0 && value !== 0.0) {
        return `>${numeral(rounded).format("0")}%`;
    }
    if (rounded === 100.0 && value !== 100.0) {
        return `<${numeral(rounded).format("0")}%`;
    }
    return `${numeral(rounded).format("0")}%`;
});

Vue.filter("formatPercentage2D", (value) => {
    const rounded = Math.round(value * 100) / 100;

    if (rounded === 0.0 && value !== 0.0) {
        return `>${numeral(rounded).format("0.00")}%`;
    }
    if (rounded === 100.0 && value !== 100.0) {
        return `<${numeral(rounded).format("0.00")}%`;
    }
    return `${numeral(rounded).format("0.00")}%`;
});
