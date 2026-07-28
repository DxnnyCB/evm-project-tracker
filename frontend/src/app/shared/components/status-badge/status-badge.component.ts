import { NgClass } from '@angular/common';
import { Component, Input } from '@angular/core';

import { CpiStatus, SpiStatus } from '../../../models/evm-status.model';

export type StatusBadgeKind = 'cpi' | 'spi';

@Component({
  selector: 'app-status-badge',
  imports: [NgClass],
  templateUrl: './status-badge.component.html',
  styleUrl: './status-badge.component.css',
})
export class StatusBadgeComponent {
  @Input({ required: true }) kind!: StatusBadgeKind;
  @Input({ required: true }) status!: CpiStatus | SpiStatus;
  /** Texto corto visible en el badge (ej. "Bajo presupuesto"). */
  @Input({ required: true }) label!: string;

  toneClass(): string {
    switch (this.status) {
      case 'under_budget':
      case 'ahead_of_schedule':
        return 'border-emerald-200 bg-emerald-50 text-emerald-800';
      case 'on_budget':
      case 'on_schedule':
        return 'border-amber-200 bg-amber-50 text-amber-900';
      case 'over_budget':
      case 'behind_schedule':
        return 'border-red-200 bg-red-50 text-red-800';
      case 'insufficient_data':
      case 'cost_not_recorded':
      case 'progress_not_recorded':
      default:
        return 'border-slate-200 bg-slate-100 text-slate-700';
    }
  }

  kindLabel(): string {
    return this.kind === 'cpi' ? 'CPI' : 'SPI';
  }
}
