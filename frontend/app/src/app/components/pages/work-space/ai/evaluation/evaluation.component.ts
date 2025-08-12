import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AiService } from '../../../../../services/ai/ai.service';

@Component({
  selector: 'app-evaluation',
  standalone: false,
  templateUrl: './evaluation.component.html',
  styleUrl: './evaluation.component.css'
})
export class EvaluationComponent implements OnInit {
  patientId: string = '';
  usefulness: boolean = true;
  satisfaction: 'Excelente' | 'Satisfactorio' | 'Neutro' | 'No satisfactorio' = 'Satisfactorio';
  comments: string = '';
  submitted = false;

  constructor(
    private route: ActivatedRoute, 
    private aiService: AiService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      this.patientId = params['patient_id'] || '';
    });
  }

  submitEvaluation() {
    const payload = {
      patient_id: this.patientId,
      usefulness: this.usefulness,
      satisfaction: this.satisfaction,
      comments: this.comments,
    };

    this.aiService.evaluateIA(payload).subscribe({
      next: () => {
        this.submitted = true;
        this.router.navigate([('/work-space/patients')])
      },
      error: (err) => {
        alert('Error al enviar evaluación: ' + err.error?.detail || 'Error desconocido');
      },
    });
  }
}

