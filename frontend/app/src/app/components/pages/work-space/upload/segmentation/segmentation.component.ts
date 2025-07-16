import { Component, OnInit } from '@angular/core';
import { AiService } from '../../../../../services/ai/ai.service';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { UploadService } from '../../../../../services/upload_files/upload.service';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-segmentation',
  standalone: false,
  templateUrl: './segmentation.component.html',
  styleUrl: './segmentation.component.css',
})
export class SegmentationComponent implements OnInit {
  patientId = '';
  files: { [key: string]: File } = {};
  fileList: File[] = [];
  error: string | null = null;
  loading = false;
  dragging = false;

  // Detección de modalidades similar al backend
  modalityKeywords: Record<string, string[]> = {
    FLAIR: ['flair', 't2f'],
    T1: ['t1', 't1n'],
    T1c: ['t1c', 't1ce'],
    T2: ['t2', 't2w'],
  };

  constructor(
    private uploadService: UploadService,
    private aiService: AiService,
    private route: ActivatedRoute
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      const id = params['patient_id'];
      if (id) {
        this.patientId = id;
      }
    });
  }

  onFileChange(event: any) {
    this.processFiles(event.target.files);
  }

  onDrop(event: DragEvent) {
    event.preventDefault();
    this.dragging = false;
    if (event.dataTransfer?.files) {
      this.processFiles(event.dataTransfer.files);
    }
  }

  onDragOver(event: DragEvent) {
    event.preventDefault();
    this.dragging = true;
  }

  onDragLeave(event: DragEvent) {
    this.dragging = false;
  }

  detectModality(filename: string): string | null {
    const normalized = filename.toLowerCase().replace(/[^a-z0-9]/g, '');
    const priority = ['T1c', 'T1', 'FLAIR', 'T2']; // Para evitar que t1c caiga como t1

    for (const mod of priority) {
      if (this.modalityKeywords[mod].some((k) => normalized.includes(k))) {
        return mod;
      }
    }

    return null;
  }

  processFiles(fileList: FileList) {
    this.error = null;
    this.files = {};

    for (const file of Array.from(fileList)) {
      const name = file.name.toLowerCase();
      if (!name.endsWith('.nii') && !name.endsWith('.nii.gz')) {
        this.error = 'Solo se permiten archivos .nii o .nii.gz';
        return;
      }

      const modality = this.detectModality(name);
      if (!modality) {
        this.error = `No se pudo detectar la modalidad de: ${file.name}`;
        return;
      }

      this.files[modality] = file; // Sobrescribe si hay repetidos
    }

    this.fileList = Object.values(this.files);

    // Ejecutar automáticamente si todo está listo
    if (this.canSubmit()) {
      this.onSubmit();
    }
  }

  canSubmit(): boolean {
    return (
      this.patientId.trim() !== '' &&
      ['T1', 'T1c', 'T2', 'FLAIR'].every((mod) => !!this.files[mod])
    );
  }

  onSubmit() {
    if (!this.canSubmit()) {
      this.error =
        'Debes subir las 4 modalidades y completar el ID del paciente.';
      return;
    }

    this.loading = true;
    this.error = null;

    const filesToSend = ['FLAIR', 'T1', 'T1c', 'T2'].map(
      (mod) => this.files[mod]
    );

    this.uploadService.uploadNiftiFiles(this.patientId, filesToSend).subscribe({
      next: (res) => {
        const folder = res.upload_folder_id;

        // Ahora segmentar
        this.aiService.segmentPatient(folder).subscribe({
          next: (result) => {
            this.loading = false;
            // Redirige a la visualización una vez generado el HTML
            window.location.href = `/ai/graphs?folder_id=${folder}`;
          },
          error: (err) => {
            this.loading = false;
            this.error = 'Error al ejecutar la segmentación.';
          },
        });
      },
      error: (err) => {
        this.loading = false;
        this.error = err.error?.detail || 'Error al subir los archivos.';
      },
    });
  }
}
