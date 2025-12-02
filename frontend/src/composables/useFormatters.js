import numeral from "numeral";

export function useFormatters() {
    const formatNumber = (value) => {
        if (value === undefined) {
            return value;
        }
        return numeral(value).format("0,0");
    };

    const formatNumber2D = (value) => {
        return numeral(value).format("0,0.00");
    };

    const formatPercentage = (value) => {
        const rounded = Math.round(value);

        if (rounded === 0.0 && value !== 0.0) {
            return `>${numeral(rounded).format("0")}%`;
        }
        if (rounded === 100.0 && value !== 100.0) {
            return `<${numeral(rounded).format("0")}%`;
        }
        return `${numeral(rounded).format("0")}%`;
    };

    const formatPercentageOmitZero = (value) => {
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
    };

    const formatPercentage2D = (value) => {
        const rounded = Math.round(value * 100) / 100;

        if (rounded === 0.0 && value !== 0.0) {
            return `>${numeral(rounded).format("0.00")}%`;
        }
        if (rounded === 100.0 && value !== 100.0) {
            return `<${numeral(rounded).format("0.00")}%`;
        }
        return `${numeral(rounded).format("0.00")}%`;
    };

    return {
        formatNumber,
        formatNumber2D,
        formatPercentage,
        formatPercentageOmitZero,
        formatPercentage2D,
    };
}
