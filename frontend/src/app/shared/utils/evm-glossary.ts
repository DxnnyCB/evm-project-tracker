/** Short Spanish glosses for EVM acronyms shown in the UI. */

export type EvmMetricCode =
  | 'BAC'
  | 'AC'
  | 'PV'
  | 'EV'
  | 'CV'
  | 'SV'
  | 'CPI'
  | 'SPI'
  | 'EAC'
  | 'VAC'
  | 'PLAN_PCT'
  | 'REAL_PCT';

export const EVM_GLOSSARY: Record<EvmMetricCode, string> = {
  BAC: 'Presupuesto a la conclusión (Budget at Completion): costo total planificado de la actividad o del proyecto.',
  AC: 'Costo real (Actual Cost): dinero ya gastado en el trabajo realizado.',
  PV: 'Valor planificado (Planned Value): BAC × avance planificado. Lo que debió ganarse según el plan.',
  EV: 'Valor ganado (Earned Value): BAC × avance real. Valor del trabajo realmente completado.',
  CV: 'Variación de costo (Cost Variance): EV − AC. Positivo = bajo presupuesto; negativo = sobre presupuesto.',
  SV: 'Variación de cronograma (Schedule Variance): EV − PV. Positivo = adelantado; negativo = atrasado.',
  CPI: 'Índice de desempeño del costo (Cost Performance Index): EV / AC. >1 bajo presupuesto; <1 sobre presupuesto.',
  SPI: 'Índice de desempeño del cronograma (Schedule Performance Index): EV / PV. >1 adelantado; <1 atrasado.',
  EAC: 'Estimación a la conclusión (Estimate at Completion): BAC / CPI. Costo total proyectado si el ritmo de gasto se mantiene.',
  VAC: 'Variación a la conclusión (Variance at Completion): BAC − EAC. Diferencia esperada entre presupuesto y proyección.',
  PLAN_PCT: 'Avance planificado: porcentaje de avance que debería llevarse a esta fecha según el plan.',
  REAL_PCT: 'Avance real: porcentaje de avance realmente completado a la fecha.',
};

export function glossaryFor(code: EvmMetricCode): string {
  return EVM_GLOSSARY[code];
}
