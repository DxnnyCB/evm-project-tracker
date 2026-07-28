import { CpiStatus, SpiStatus } from './evm-status.model';

/**
 * Money / progress / index fields mirror FastAPI `Decimal` JSON as `string`
 * (e.g. `"8000000.00"`, `"0.93"`). `null` when the index is indeterminate.
 */

/** Mirrors `ActivityIndicatorsSchema`. */
export interface ActivityIndicators {
  pv: string;
  ev: string;
  cv: string;
  sv: string;
  cpi: string | null;
  spi: string | null;
  eac: string | null;
  vac: string | null;
  cpi_status: CpiStatus;
  cpi_message: string;
  spi_status: SpiStatus;
  spi_message: string;
}

/** Mirrors `ActivityRead`. */
export interface Activity {
  id: number;
  project_id: number;
  name: string;
  bac: string;
  planned_progress: string;
  actual_progress: string;
  ac: string;
}

/** Mirrors `ActivityWithIndicators`. */
export interface ActivityWithIndicators extends Activity {
  indicators: ActivityIndicators;
}

/** Mirrors `ActivityCreate`. */
export interface ActivityCreate {
  name: string;
  bac: string;
  planned_progress: string;
  actual_progress: string;
  ac: string;
}

/** Mirrors `ActivityUpdate` (all fields optional). */
export interface ActivityUpdate {
  name?: string;
  bac?: string;
  planned_progress?: string;
  actual_progress?: string;
  ac?: string;
}
