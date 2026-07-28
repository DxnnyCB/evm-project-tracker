import { AsyncPipe, NgClass } from '@angular/common';
import { Component, inject } from '@angular/core';

import { ToastService } from '../../services/toast.service';

@Component({
  selector: 'app-toast-container',
  imports: [AsyncPipe, NgClass],
  templateUrl: './toast-container.component.html',
})
export class ToastContainerComponent {
  readonly toastService = inject(ToastService);
}
