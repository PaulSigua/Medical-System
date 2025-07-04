import { Component } from '@angular/core';
import { AiService } from '../../../../../services/ai/ai.service';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

@Component({
  selector: 'app-segmentation',
  standalone: false,
  templateUrl: './segmentation.component.html',
  styleUrl: './segmentation.component.css',
})
export class SegmentationComponent {
  patientId = '';
  files: { [key: string]: File } = {};
  fileList: File[] = [];
  segmentationUrl: SafeResourceUrl | null = null;
  error: string | null = null;
  loading = false;
  dragging = false;

  constructor(private aiService: AiService, private sanitizer: DomSanitizer) {}

  allowedModalities = ['T1c', 'T2W', 'T2F'];

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

  processFiles(fileList: FileList) {
    this.error = null;
    for (const file of Array.from(fileList)) {
      const name = file.name.toLowerCase();
      if (!name.endsWith('.nii.gz')) {
        this.error = 'Solo se permiten archivos con extensión .nii.gz';
        return;
      }

      for (const modality of this.allowedModalities) {
        if (name.includes(modality.toLowerCase())) {
          this.files[modality] = file;
          break;
        }
      }
    }

    // Mostrar lista
    this.fileList = Object.values(this.files);
  }

  canSubmit(): boolean {
    return (
      this.patientId.trim() !== '' &&
      this.allowedModalities.every((mod) => !!this.files[mod])
    );
  }

  onSubmit() {
    if (!this.canSubmit()) {
      this.error =
        'Completa todos los campos y sube todas las modalidades requeridas.';
      return;
    }

    this.loading = true;
    this.error = null;

    this.aiService
      .segmentTumor(this.patientId, {
        T1c: this.files['T1c'],
        T2W: this.files['T2W'],
        T2F: this.files['T2F'],
      })
      .subscribe({
        next: (res: any) => {
          this.loading = false;
          // Redirigir a la visualización de resultados
          window.location.href = `/ia/graphs?patient_id=${this.patientId}`;
        },
        error: () => {
          this.error = 'Error al procesar la segmentación.';
          this.loading = false;
        },
      });
  }
}
