import { Component, OnInit } from '@angular/core';
import { Brain, PersonStanding, User } from 'lucide-angular';
import { AiService } from '../../../../services/ai/ai.service';
import { InfoService } from '../../../../services/user/info.service';

@Component({
  selector: 'app-home',
  standalone: false,
  templateUrl: './home.component.html',
  styleUrl: './home.component.css',
})
export class HomeComponent implements OnInit {
  icons = {
    PersonStanding,
    Brain,
  };

  satisfactionLabels = [
    'Excelente',
    'Satisfactorio',
    'Neutro',
    'No satisfactorio',
  ];
  satisfactionData: any[] = [];
  totalPredictions = 0;
  totalPatients = 0;
  lastPrediction: string | null = null;

  constructor(
    private aiService: AiService,
    private reportsService: InfoService
  ) {}

  ngOnInit(): void {
    this.aiService.getSatisfactionSummary().subscribe((res) => {
      const values = this.satisfactionLabels.map((label) => res[label] || 0);

      // console.log(values);
      this.satisfactionData = [
        {
          label: 'Evaluación de IA',
          data: values,
          backgroundColor: values.map((_, i) =>
            this.getColorForLabel(this.satisfactionLabels[i])
          ),
        },
      ];
    });
    this.reportsService.getStatistics().subscribe({
      next: (data) => {
        this.totalPredictions = data.total_predictions;
        this.totalPatients = data.total_patients;
        this.lastPrediction = data.last_prediction;
      },
      error: (err) => {
        console.error('Error al cargar estadísticas:', err);
      }
    });
  }
  getColorForLabel(label: string): string {
    switch (label) {
      case 'Excelente':
        return '#10B981';
      case 'Satisfactorio':
        return '#3B82F6';
      case 'Neutro':
        return '#F59E0B';
      case 'No satisfactorio':
        return '#EF4444';
      default:
        return '#94A3B8';
    }
  }
}
