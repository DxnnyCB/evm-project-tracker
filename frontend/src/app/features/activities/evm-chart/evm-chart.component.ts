import {
  AfterViewInit,
  Component,
  ElementRef,
  Input,
  OnChanges,
  OnDestroy,
  SimpleChanges,
  ViewChild,
} from '@angular/core';
import { Chart, ChartConfiguration, registerables } from 'chart.js';

import { ActivityWithIndicators } from '../../../models/activity.model';
import { formatMoney, formatMoneyCompact } from '../../../shared/utils/format';

Chart.register(...registerables);

/** Máximo de actividades en el chart para que siga siendo legible de un vistazo. */
const MAX_CHART_ACTIVITIES = 10;

@Component({
  selector: 'app-evm-chart',
  imports: [],
  templateUrl: './evm-chart.component.html',
  styleUrl: './evm-chart.component.css',
})
export class EvmChartComponent implements AfterViewInit, OnChanges, OnDestroy {
  @Input({ required: true }) activities: ActivityWithIndicators[] = [];

  @ViewChild('chartCanvas') private chartCanvas?: ElementRef<HTMLCanvasElement>;

  private chart: Chart | null = null;
  private viewReady = false;

  /** Actividades que se dibujan (todas o top N por |CV|). */
  chartActivities: ActivityWithIndicators[] = [];

  ngAfterViewInit(): void {
    this.viewReady = true;
    this.scheduleRender();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['activities']) {
      this.chartActivities = this.selectActivitiesForChart(this.activities);
      if (this.viewReady) {
        // Esperar un tick para que el canvas exista si el *ngIf acaba de activarse.
        this.scheduleRender();
      }
    }
  }

  ngOnDestroy(): void {
    this.destroyChart();
  }

  get hasActivities(): boolean {
    return this.activities.length > 0;
  }

  get isTruncated(): boolean {
    return this.activities.length > MAX_CHART_ACTIVITIES;
  }

  get shownCount(): number {
    return this.chartActivities.length;
  }

  get totalCount(): number {
    return this.activities.length;
  }

  private selectActivitiesForChart(
    activities: ActivityWithIndicators[],
  ): ActivityWithIndicators[] {
    if (activities.length <= MAX_CHART_ACTIVITIES) {
      return [...activities];
    }

    return [...activities]
      .sort((a, b) => {
        const diff =
          Math.abs(this.toNumber(b.indicators.cv)) -
          Math.abs(this.toNumber(a.indicators.cv));
        if (diff !== 0) {
          return diff;
        }
        return a.id - b.id;
      })
      .slice(0, MAX_CHART_ACTIVITIES);
  }

  private scheduleRender(): void {
    setTimeout(() => this.renderChart(), 0);
  }

  private renderChart(): void {
    if (!this.viewReady || !this.chartCanvas || !this.hasActivities) {
      this.destroyChart();
      return;
    }

    const labels = this.chartActivities.map((activity) => activity.name);
    const pv = this.chartActivities.map((activity) =>
      this.toNumber(activity.indicators.pv),
    );
    const ev = this.chartActivities.map((activity) =>
      this.toNumber(activity.indicators.ev),
    );
    const ac = this.chartActivities.map((activity) => this.toNumber(activity.ac));

    const config: ChartConfiguration<'bar'> = {
      type: 'bar',
      data: {
        labels,
        datasets: [
          {
            label: 'PV',
            data: pv,
            backgroundColor: 'rgba(71, 85, 105, 0.75)',
            borderColor: 'rgb(71, 85, 105)',
            borderWidth: 1,
          },
          {
            label: 'EV',
            data: ev,
            backgroundColor: 'rgba(4, 120, 87, 0.75)',
            borderColor: 'rgb(4, 120, 87)',
            borderWidth: 1,
          },
          {
            label: 'AC',
            data: ac,
            backgroundColor: 'rgba(185, 28, 28, 0.7)',
            borderColor: 'rgb(185, 28, 28)',
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: false,
          },
          tooltip: {
            callbacks: {
              label: (context) => {
                const value = context.parsed.y;
                return `${context.dataset.label}: ${formatMoney(value)}`;
              },
            },
          },
        },
        scales: {
          x: {
            title: {
              display: true,
              text: 'Actividad',
            },
          },
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Valor (COP)',
            },
            ticks: {
              callback: (value) =>
                typeof value === 'number' ? formatMoneyCompact(value) : value,
            },
          },
        },
      },
    };

    this.destroyChart();
    this.chart = new Chart(this.chartCanvas.nativeElement, config);
  }

  private destroyChart(): void {
    if (this.chart) {
      this.chart.destroy();
      this.chart = null;
    }
  }

  private toNumber(raw: string): number {
    const value = Number(raw);
    return Number.isFinite(value) ? value : 0;
  }
}
