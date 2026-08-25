import { computed } from "vue";
import { useI18n } from "vue-i18n";

export function useFormatters() {
  const { locale } = useI18n();

  // A user reading the interface in Spanish reads 12.047 and 25,5 %, not 12,047 and 25.5%.
  const integer = computed(() => new Intl.NumberFormat(locale.value, { maximumFractionDigits: 0 }));

  const formatNumber = (value: number | undefined) => {
    if (value === undefined) {
      return value;
    }
    return integer.value.format(value);
  };

  const percentFormatter = (digits: number) => {
    const formatter = computed(
      () =>
        new Intl.NumberFormat(locale.value, {
          style: "percent",
          minimumFractionDigits: digits,
          maximumFractionDigits: digits,
        }),
    );
    const factor = 10 ** (digits + 2);

    // A percentage that rounds to 0 or 100 without being either is reported as short of it.
    return (value: number) => {
      const rounded = Math.round(value * factor) / factor;

      if (rounded === 0 && value !== 0) {
        return `>${formatter.value.format(0)}`;
      }
      if (rounded === 1 && value !== 1) {
        return `<${formatter.value.format(1)}`;
      }
      return formatter.value.format(value);
    };
  };

  return {
    formatNumber,
    formatPercentage: percentFormatter(0),
    formatPercentage2D: percentFormatter(2),
  };
}
