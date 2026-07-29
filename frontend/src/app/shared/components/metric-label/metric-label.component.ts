import { Component, Input } from '@angular/core';

import { EvmMetricCode, glossaryFor } from '../../utils/evm-glossary';

let nextTipId = 0;

@Component({
  selector: 'app-metric-label',
  templateUrl: './metric-label.component.html',
})
export class MetricLabelComponent {
  @Input({ required: true }) code!: EvmMetricCode;
  /** Visible label; defaults to the metric code. */
  @Input() label?: string;

  readonly tipId = `metric-tip-${++nextTipId}`;

  get displayLabel(): string {
    return this.label ?? this.code;
  }

  get description(): string {
    return glossaryFor(this.code);
  }
}
