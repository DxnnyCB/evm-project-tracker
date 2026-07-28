import {
  Component,
  EventEmitter,
  Input,
  OnChanges,
  Output,
  SimpleChanges,
} from '@angular/core';
import { FormsModule } from '@angular/forms';

import {
  ActivityCreate,
  ActivityWithIndicators,
} from '../../../models/activity.model';

export interface ActivityFormSaveEvent {
  /** Present when updating an existing activity. */
  activityId: number | null;
  data: ActivityCreate;
}

@Component({
  selector: 'app-activity-form',
  imports: [FormsModule],
  templateUrl: './activity-form.component.html',
  styleUrl: './activity-form.component.css',
})
export class ActivityFormComponent implements OnChanges {
  /** When set, the form opens in edit mode and loads the activity fields. */
  @Input() activity: ActivityWithIndicators | null = null;
  @Input() saving = false;

  @Output() readonly save = new EventEmitter<ActivityFormSaveEvent>();
  @Output() readonly cancel = new EventEmitter<void>();

  expanded = false;
  name = '';
  bac = '';
  plannedProgress = '';
  actualProgress = '';
  ac = '';
  validationError: string | null = null;

  get isEditMode(): boolean {
    return this.activity !== null;
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['activity']) {
      if (this.activity) {
        this.expanded = true;
        this.fillFromActivity(this.activity);
      } else if (!changes['activity'].firstChange) {
        this.resetFields();
      }
    }
  }

  openForCreate(): void {
    this.expanded = true;
    this.validationError = null;
    this.resetFields();
    if (this.activity) {
      this.cancel.emit();
    }
  }

  /** Called by the parent after a successful save. */
  close(): void {
    this.expanded = false;
    this.validationError = null;
    this.resetFields();
  }

  onCancel(): void {
    this.close();
    this.cancel.emit();
  }

  onSubmit(): void {
    this.validationError = null;
    const data = this.buildPayload();
    if (!data) {
      return;
    }
    this.save.emit({
      activityId: this.activity?.id ?? null,
      data,
    });
  }

  private fillFromActivity(activity: ActivityWithIndicators): void {
    this.name = activity.name;
    this.bac = activity.bac;
    this.plannedProgress = activity.planned_progress;
    this.actualProgress = activity.actual_progress;
    this.ac = activity.ac;
    this.validationError = null;
  }

  private resetFields(): void {
    this.name = '';
    this.bac = '';
    this.plannedProgress = '';
    this.actualProgress = '';
    this.ac = '';
  }

  private buildPayload(): ActivityCreate | null {
    const name = this.name.trim();
    if (!name) {
      this.validationError = 'El nombre es obligatorio.';
      return null;
    }

    const bac = this.parseNumber(this.bac, 'BAC');
    if (bac === null) {
      return null;
    }
    if (bac <= 0) {
      this.validationError = 'BAC debe ser mayor que 0.';
      return null;
    }

    const planned = this.parseNumber(this.plannedProgress, 'Avance planificado');
    if (planned === null) {
      return null;
    }
    if (planned < 0 || planned > 100) {
      this.validationError = 'El avance planificado debe estar entre 0 y 100.';
      return null;
    }

    const actual = this.parseNumber(this.actualProgress, 'Avance real');
    if (actual === null) {
      return null;
    }
    if (actual < 0 || actual > 100) {
      this.validationError = 'El avance real debe estar entre 0 y 100.';
      return null;
    }

    const ac = this.parseNumber(this.ac, 'AC');
    if (ac === null) {
      return null;
    }
    if (ac < 0) {
      this.validationError = 'AC no puede ser negativo.';
      return null;
    }

    return {
      name,
      bac: this.asDecimalString(bac),
      planned_progress: this.asDecimalString(planned),
      actual_progress: this.asDecimalString(actual),
      ac: this.asDecimalString(ac),
    };
  }

  private parseNumber(raw: string, fieldLabel: string): number | null {
    const trimmed = raw.trim().replace(',', '.');
    if (!trimmed) {
      this.validationError = `${fieldLabel} es obligatorio.`;
      return null;
    }
    const value = Number(trimmed);
    if (!Number.isFinite(value)) {
      this.validationError = `${fieldLabel} no es un número válido.`;
      return null;
    }
    return value;
  }

  /** Keep API contract as string Decimals without float noise. */
  private asDecimalString(value: number): string {
    return String(value);
  }
}
