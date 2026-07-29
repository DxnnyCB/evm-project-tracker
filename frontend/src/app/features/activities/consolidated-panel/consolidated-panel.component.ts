import { Component, Input } from '@angular/core';

import { StatusBadgeComponent } from '../../../shared/components/status-badge/status-badge.component';
import { ProjectConsolidatedIndicators } from '../../../models/project.model';
import { formatIndex, formatMoney } from '../../../shared/utils/format';

@Component({
  selector: 'app-consolidated-panel',
  imports: [StatusBadgeComponent],
  templateUrl: './consolidated-panel.component.html',
  styleUrl: './consolidated-panel.component.css',
})
export class ConsolidatedPanelComponent {
  @Input({ required: true }) consolidated!: ProjectConsolidatedIndicators;

  readonly formatMoney = formatMoney;
  readonly formatIndex = formatIndex;

  cpiLabel(): string {
    switch (this.consolidated.cpi_status) {
      case 'under_budget':
        return 'Bajo presupuesto';
      case 'over_budget':
        return 'Sobre presupuesto';
      case 'on_budget':
        return 'En presupuesto';
      case 'cost_not_recorded':
        return 'Sin costo registrado';
      case 'insufficient_data':
      default:
        return 'Datos insuficientes';
    }
  }

  spiLabel(): string {
    switch (this.consolidated.spi_status) {
      case 'ahead_of_schedule':
        return 'Adelantado';
      case 'behind_schedule':
        return 'Atrasado';
      case 'on_schedule':
        return 'En cronograma';
      case 'progress_not_recorded':
        return 'Sin avance planificado';
      case 'insufficient_data':
      default:
        return 'Datos insuficientes';
    }
  }
}
