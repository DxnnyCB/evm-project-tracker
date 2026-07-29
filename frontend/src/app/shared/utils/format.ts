/** Presentational helpers — do not use for API payloads. */

const moneyFormatter = new Intl.NumberFormat('es-CO', {
  style: 'currency',
  currency: 'COP',
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
});

const moneyAxisFormatter = new Intl.NumberFormat('es-CO', {
  style: 'currency',
  currency: 'COP',
  notation: 'compact',
  maximumFractionDigits: 1,
});

export function formatMoney(value: string | number | null | undefined): string {
  if (value === null || value === undefined || value === '') {
    return '—';
  }
  const n = typeof value === 'number' ? value : Number(value);
  if (!Number.isFinite(n)) {
    return '—';
  }
  return moneyFormatter.format(n);
}

/** Compact COP for chart axes (e.g. $8,0 M). */
export function formatMoneyCompact(value: number): string {
  if (!Number.isFinite(value)) {
    return '—';
  }
  return moneyAxisFormatter.format(value);
}

export function formatIndex(value: string | null | undefined): string {
  return value ?? '—';
}
