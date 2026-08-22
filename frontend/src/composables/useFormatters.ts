import { computed } from "vue";
import { useI18n } from "vue-i18n";

export function useFormatters() {
  const { locale } = useI18n();

  // A reader who reads the interface in Spanish reads 12.047 and 0,25, not 12,047 and 0.25.
  const integer = computed(() => new Intl.NumberFormat(locale.value, { maximumFractionDigits: 0 }));
  const twoDecimals = computed(
    () => new Intl.NumberFormat(locale.value, { minimumFractionDigits: 2, maximumFractionDigits: 2 }),
  );

  const formatNumber = (value: number | undefined) => {
    if (value === undefined) {
      return value;
    }
    return integer.value.format(value);
  };

  // A percentage that rounds to 0 or 100 without being either is reported as short of it.
  const formatPercentage = (value: number) => {
    const percentage = value * 100;
    const rounded = Math.round(percentage);

    if (rounded === 0.0 && percentage !== 0.0) {
      return `>${integer.value.format(rounded)}%`;
    }
    if (rounded === 100.0 && percentage !== 100.0) {
      return `<${integer.value.format(rounded)}%`;
    }
    return `${integer.value.format(rounded)}%`;
  };

  const formatPercentage2D = (value: number) => {
    const percentage = value * 100;
    const rounded = Math.round(percentage * 100) / 100;

    if (rounded === 0.0 && percentage !== 0.0) {
      return `>${twoDecimals.value.format(rounded)}%`;
    }
    if (rounded === 100.0 && percentage !== 100.0) {
      return `<${twoDecimals.value.format(rounded)}%`;
    }
    return `${twoDecimals.value.format(rounded)}%`;
  };

  return {
    formatNumber,
    formatPercentage,
    formatPercentage2D,
  };
}
