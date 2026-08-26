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

  // The sign stays attached in every language, as elsewhere in the interface, rather than
  // spaced off as Intl's percent style would in Spanish.
  const percentFormatter = (digits: number) => {
    const formatter = computed(
      () => new Intl.NumberFormat(locale.value, { minimumFractionDigits: digits, maximumFractionDigits: digits }),
    );
    const factor = 10 ** digits;

    // A percentage that rounds to 0 or 100 without being either is reported as short of it.
    return (value: number) => {
      const percentage = value * 100;
      const rounded = Math.round(percentage * factor) / factor;

      if (rounded === 0 && percentage !== 0) {
        return `>${formatter.value.format(0)}%`;
      }
      if (rounded === 100 && percentage !== 100) {
        return `<${formatter.value.format(100)}%`;
      }
      return `${formatter.value.format(rounded)}%`;
    };
  };

  return {
    formatNumber,
    formatPercentage: percentFormatter(0),
    formatPercentage2D: percentFormatter(2),
  };
}
