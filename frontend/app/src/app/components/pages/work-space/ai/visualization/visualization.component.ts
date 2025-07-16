import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { environment } from '../../../../../../environments/environment.development';
import { AiService } from '../../../../../services/ai/ai.service';
import { DiagnosticForm } from '../../../../../models/diagnostics';

@Component({
  selector: 'app-visualization',
  standalone: false,
  templateUrl: './visualization.component.html',
  styleUrl: './visualization.component.css',
})
export class VisualizationComponent implements OnInit {
  iframeUrl: SafeResourceUrl | null = null;
  summaryImageUrl: SafeResourceUrl | null = null;
  classDistImageUrl: SafeResourceUrl | null = null;
  isLoading = true;
  error: string | null = null;
  diceScores: any = null;
  allMetrics: any = null;

  diagnosticSelected: string = '';
  observations: string = '';
  explanation: string | null = null;

  constructor(
    private route: ActivatedRoute,
    private sanitizer: DomSanitizer,
    private aiService: AiService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      const folderId = params['folder_id'];
      if (!folderId) {
        this.error = 'No se proporcionó el folder_id.';
        this.isLoading = false;
        return;
      }

      // Ejecutar segmentación solo si se necesita la respuesta con métricas
      this.isLoading = true;
      this.aiService.segmentPatient(folderId).subscribe({
      next: (res) => {
        const backendBase = environment.BACKEND_URL;

        this.iframeUrl = this.sanitizer.bypassSecurityTrustResourceUrl(
          `${backendBase}${res.segmentation_url}`
        );
        this.summaryImageUrl = this.sanitizer.bypassSecurityTrustResourceUrl(
          `${backendBase}${res.summary_image_url}`
        );
        this.classDistImageUrl = this.sanitizer.bypassSecurityTrustResourceUrl(
          `${backendBase}${res.class_distribution_url}`
        );

        this.diceScores = res.metrics?.dice_score || null;
        this.allMetrics = res.metrics?.all_metrics || null;
        this.explanation = res.explanation || null;
      },
        error: (err) => {
          this.error =
            err.error?.detail || 'Error al cargar la segmentación.';
          this.isLoading = false;
        },
        complete: () => {
          this.isLoading = false;
        },
      });
    });
  }

  onIframeLoad() {
    this.isLoading = false;
  }

  diceLabels(): string[] {
    return Object.keys(this.diceScores || {});
  }

  metricLabels(): string[] {
    return Object.keys(this.allMetrics || {});
  }

  metricKeys(label: string): string[] {
    return Object.keys(this.allMetrics?.[label] || {});
  }

  sendForm() {
    const folderId = this.route.snapshot.queryParamMap.get('folder_id') || '';
    const match = folderId.match(/_(\d{10})/);
    const patientId = match ? match[1] : '';

    if (!this.diagnosticSelected || !this.observations || !patientId) {
      alert('Por favor, complete todos los campos del formulario.');
      return;
    }
    const payload: DiagnosticForm = {
      patient_id: patientId,
      description: this.observations,
      diagnostic: this.diagnosticSelected,
    };

    this.aiService.saveDiagnostic(payload).subscribe({
      next: () => {
        alert('Formulario enviado correctamente.');
        this.diagnosticSelected = '';
        this.observations = '';
        this.router.navigate(['/work-space/patients']);
      },
      error: (err) => {
        console.error('Error al enviar formulario:', err);
        alert('Ocurrió un error al enviar el diagnóstico.');
      },
    });
  }
}
