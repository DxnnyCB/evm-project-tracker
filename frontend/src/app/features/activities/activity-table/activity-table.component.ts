import { Component, EventEmitter, Input, Output } from '@angular/core';

import { StatusBadgeComponent } from '../../../shared/components/status-badge/status-badge.component';
import { ActivityWithIndicators } from '../../../models/activity.model';
import { CpiStatus, SpiStatus } from '../../../models/evm-status.model';

@Component({
  selector: 'app-activity-table',
  imports: [StatusBadgeComponent],
  templateUrl: './activity-table.component.html',
  styleUrl: './activity-table.component.css',
})
export class ActivityTableComponent {
  @Input({ required: true }) activities: ActivityWithIndicators[] = [];

  @Output() readonly edit = new EventEmitter<ActivityWithIndicators>();
  @Output() readonly remove = new EventEmitter<ActivityWithIndicators>();

  formatIndex(value: string | null): string {
    return value ?? '—';
  }

  cpiLabel(status: CpiStatus): string {
    switch (status) {
      case 'under_budget':
        return 'Bajo presupuesto';
      case 'over_budget':
        return 'Sobre presupuesto';
      case 'on_budget':
        return 'En presupuesto';
      case 'cost_not_recorded':
        return 'Sin costo';
      case 'insufficient_data':
      default:
        return 'Sin datos';
    }
  }

  spiLabel(status: SpiStatus): string {
    switch (status) {
      case 'ahead_of_schedule':
        return 'Adelantado';
      case 'behind_schedule':
        return 'Atrasado';
      case 'on_schedule':
        return 'En cronograma';
      case 'progress_not_recorded':
        return 'Sin avance';
      case 'insufficient_data':
      default:
        return 'Sin datos';
    }
  }

  onEdit(activity: ActivityWithIndicators): void {
    this.edit.emit(activity);
  }

  onRemove(activity: ActivityWithIndicators): void {
    this.remove.emit(activity);
  }
}
