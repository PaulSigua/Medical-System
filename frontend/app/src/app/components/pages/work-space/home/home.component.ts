import { Component, OnInit } from '@angular/core';
import { Brain, PersonStanding, User } from 'lucide-angular';
import { AiService } from '../../../../services/ai/ai.service';

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

  constructor(private aiService: AiService) {}

  ngOnInit(): void {
    this.aiService.getSatisfactionSummary().subscribe((res) => {
      const values = this.satisfactionLabels.map((label) => res[label] || 0);

      console.log(values);
      this.satisfactionData = [
        {
          label: 'Evaluación de IA',
          data: values, // ← como [0, 2, 2, 1]
          backgroundColor: values.map((_, i) =>
            this.getColorForLabel(this.satisfactionLabels[i])
          ),
        },
      ];
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
