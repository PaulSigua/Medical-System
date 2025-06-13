import { AfterViewInit, Component, ElementRef, Input, ViewChild } from '@angular/core';
import {
  Chart,
  ChartConfiguration,
  ChartDataset,
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
  @Input() data: ChartDataset<'bar'>[] = [];
  @Input() options: ChartConfiguration<'bar'>['options'] = {};

  @ViewChild('chartCanvas', { static: true }) chartCanvas!: ElementRef<HTMLCanvasElement>;
  chart?: Chart<'bar'>;

  ngAfterViewInit(): void {
    const ctx = this.chartCanvas.nativeElement.getContext('2d');
    if (ctx) {
      this.chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: this.labels,
          datasets: this.data
        },
        options: this.options
      });
    }
  }
}

