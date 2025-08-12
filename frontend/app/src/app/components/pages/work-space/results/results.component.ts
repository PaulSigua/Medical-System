import { Component } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { InfoService } from '../../../../services/user/info.service';

@Component({
  selector: 'app-results',
  standalone: false,
  templateUrl: './results.component.html',
  styleUrl: './results.component.css'
})
export class ResultsComponent {
  patientId: string = '';
  pdfUrl: SafeResourceUrl | null = null;
  loading = false;
  error: string | null = null;

  constructor(
    private reportService: InfoService,
    private sanitizer: DomSanitizer
  ) {}

  loadPdf() {
    if (!this.patientId) return;

    this.loading = true;
    this.error = null;

    this.reportService.generateReport(this.patientId).subscribe({
      next: (blob) => {
        const objectUrl = URL.createObjectURL(blob);
        this.pdfUrl = this.sanitizer.bypassSecurityTrustResourceUrl(objectUrl);
        this.loading = false;
      },
      error: () => {
        this.error = 'No se pudo cargar el reporte. Verifica el ID del paciente.';
        this.loading = false;
        this.pdfUrl = null;
      },
    });
  }
}
