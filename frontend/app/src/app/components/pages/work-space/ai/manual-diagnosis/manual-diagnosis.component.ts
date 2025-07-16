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

    const payload = {
      patient_id: this.patientId,
      description: this.observations,
      diagnostic: this.diagnosticOk === 'true' ? 'Adecuada' : 'Incorrecta',
    };

    this.aiService.saveDiagnostic(payload).subscribe({
      next: () => {
        alert('Diagnóstico guardado correctamente.');
        this.diagnosticOk = '';
        this.observations = '';
        this.router.navigate([('/work-space/patients')])
      },
      error: (err) => {
        console.error('Error al guardar diagnóstico:', err);
        alert('Ocurrió un error al guardar el diagnóstico.');
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
