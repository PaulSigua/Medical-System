import { Component, OnInit } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { ActivatedRoute, Router } from '@angular/router';
import { AiService } from '../../../../../services/ai/ai.service';
import { environment } from '../../../../../../environments/environment.development';
import { Patients } from '../../../../../models/models';

@Component({
  selector: 'app-manual-diagnosis',
  standalone: false,
  templateUrl: './manual-diagnosis.component.html',
  styleUrl: './manual-diagnosis.component.css',
})
export class ManualDiagnosisComponent implements OnInit {
  patientId = '';
  comparisonUrl: SafeResourceUrl | null = null;
  loading = false;
  error: string | null = null;

  diagnosticOk: string = '';
  observations: string = '';

  constructor(
    private route: ActivatedRoute,
    private aiService: AiService,
    private sanitizer: DomSanitizer,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      this.patientId = params['patient_id'] || '';
      if (this.patientId) {
        this.loadComparison();
      } else {
        this.error = 'ID de paciente no proporcionado.';
      }
    });
  }

  submitDiagnosis() {
    if (!this.patientId || !this.diagnosticOk || !this.observations) {
      alert('Por favor, complete todos los campos del formulario.');
      return;
    }

    const evaluationPayload = {
      patient_id: this.patientId,
      is_accurate: this.diagnosticOk as 'Sí' | 'Neutro' | 'No',
      observations: this.observations,
    };

    // Primero guarda la evaluación manual
    this.aiService.saveManualEvaluation(evaluationPayload).subscribe({
      next: () => {
        alert('Evaluación registrada correctamente.');
        this.router.navigate(['/work-space/patients']);
      },
      error: (err) => {
        console.error('Error al registrar evaluación:', err);
        alert('Ocurrió un error al registrar la evaluación.');
      },
    });
  }

  loadComparison() {
    this.loading = true;
    this.aiService.generateComparisonByPatient(this.patientId).subscribe({
      next: (res) => {
        this.comparisonUrl = this.sanitizer.bypassSecurityTrustResourceUrl(
          `${environment.BACKEND_URL}${res.comparison_url}`
        );
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Error al cargar comparación.';
        this.loading = false;
      },
    });
  }
}
