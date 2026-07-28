import { NgClass } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';

export type ConfirmDialogTone = 'danger' | 'neutral';

@Component({
  selector: 'app-confirm-dialog',
  imports: [NgClass],
  templateUrl: './confirm-dialog.component.html',
})
export class ConfirmDialogComponent {
  @Input({ required: true }) open = false;
  @Input({ required: true }) title = '';
  @Input({ required: true }) message = '';
  @Input() confirmLabel = 'Confirmar';
  @Input() cancelLabel = 'Cancelar';
  @Input() tone: ConfirmDialogTone = 'danger';

  @Output() readonly confirm = new EventEmitter<void>();
  @Output() readonly cancel = new EventEmitter<void>();

  onConfirm(): void {
    this.confirm.emit();
  }

  onCancel(): void {
    this.cancel.emit();
  }

  onBackdropClick(): void {
    this.cancel.emit();
  }
}
