import { AfterViewInit, Component, ElementRef, Input, ViewChild } from '@angular/core';
import {
  Chart,
  ChartConfiguration,
  ChartType,
  registerables
} from 'chart.js';


Chart.register(...registerables);

@Component({
  selector: 'app-histogram',
  standalone: false,
  templateUrl: './histogram.component.html',
  styleUrl: './histogram.component.css'
})
export class HistogramComponent implements AfterViewInit {
  @Input() labels: string[] = [];
  @Input() chartTradicional: ChartConfiguration['data']['datasets'] = [];
  @Input() chartAvanzada: ChartConfiguration['data']['datasets'] = [];
  @Input() options: ChartConfiguration['options'] = {};

  @ViewChild('chartCanvas1') chartCanvas1!: ElementRef<HTMLCanvasElement>;
  @ViewChild('chartCanvas2') chartCanvas2!: ElementRef<HTMLCanvasElement>;

  chart1?: Chart;
  chart2?: Chart;

  ngAfterViewInit(): void {
    if (this.chartCanvas1 && this.chartTradicional.length) {
      this.chart1 = new Chart(this.chartCanvas1.nativeElement, {
        type: 'bar' as ChartType,
        data: {
          labels: this.labels,
          datasets: this.chartTradicional
        },
        options: this.options
      });
    }

    if (this.chartCanvas2 && this.chartAvanzada.length) {
      this.chart2 = new Chart(this.chartCanvas2.nativeElement, {
        type: 'bar' as ChartType,
        data: {
          labels: this.labels,
          datasets: this.chartAvanzada
        },
        options: this.options
      });
    }
  }
}

