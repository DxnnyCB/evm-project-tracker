import { ActivityWithIndicators } from './activity.model';
import { CpiStatus, SpiStatus } from './evm-status.model';

/**
 * Money / index fields mirror FastAPI `Decimal` JSON as `string`.
 * `null` when the index is indeterminate.
 */

/** Mirrors `ProjectRead`. */
export interface Project {
  id: number;
  name: string;
}

/** Mirrors `ProjectCreate`. */
export interface ProjectCreate {
  name: string;
}

/** Mirrors `ProjectUpdate`. */
export interface ProjectUpdate {
  name?: string;
}

/** Mirrors `ProjectConsolidatedIndicatorsSchema`. */
export interface ProjectConsolidatedIndicators {
  total_bac: string;
  total_pv: string;
  total_ev: string;
  total_ac: string;
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

/** Mirrors `ProjectDetail` — project + activities with EVM + consolidated. */
export interface ProjectDetail extends Project {
  activities: ActivityWithIndicators[];
  consolidated: ProjectConsolidatedIndicators;
}
