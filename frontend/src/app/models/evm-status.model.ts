/** Mirrors `CpiStatus` from `app.services.evm.enums`. */
export type CpiStatus =
  | 'under_budget'
  | 'over_budget'
  | 'on_budget'
  | 'insufficient_data'
  | 'cost_not_recorded';

/** Mirrors `SpiStatus` from `app.services.evm.enums`. */
export type SpiStatus =
  | 'ahead_of_schedule'
  | 'behind_schedule'
  | 'on_schedule'
  | 'insufficient_data'
  | 'progress_not_recorded';
