import numeral from "numeral";

export function useFormatters() {
    const formatNumber = (value) => {
        if (value === undefined) {
            return value;
        }
        return numeral(value).format("0,0");
    };

    const formatPercentage = (value) => {
        const percentage = value * 100;
        const rounded = Math.round(percentage);

        if (rounded === 0.0 && percentage !== 0.0) {
            return `>${numeral(rounded).format("0")}%`;
        }
        if (rounded === 100.0 && percentage !== 100.0) {
            return `<${numeral(rounded).format("0")}%`;
        }
        return `${numeral(rounded).format("0")}%`;
    };

    const formatPercentage2D = (value) => {
        const percentage = value * 100;
        const rounded = Math.round(percentage * 100) / 100;

        if (rounded === 0.0 && percentage !== 0.0) {
            return `>${numeral(rounded).format("0.00")}%`;
        }
        if (rounded === 100.0 && percentage !== 100.0) {
            return `<${numeral(rounded).format("0.00")}%`;
        }
        return `${numeral(rounded).format("0.00")}%`;
    };

    return {
        formatNumber,
        formatPercentage,
        formatPercentage2D,
    };
}
