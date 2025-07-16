import { Component, OnInit } from '@angular/core';
import { UploadService } from '../../../../../services/upload_files/upload.service';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-upload-manual',
  standalone: false,
  templateUrl: './upload-manual.component.html',
  styleUrl: './upload-manual.component.css',
})
export class UploadManualComponent implements OnInit {
  manualFile: File | null = null;
  manualFileName = '';
  patientId = '';
  loading = false;

  constructor(
    private uploadService: UploadService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      const id = params['patient_id'];
      if (id) {
        this.patientId = id;
      }
    });
  }

  onManualFileChange(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.manualFile = file;
      this.manualFileName = file.name;

      if (this.patientId) {
        this.uploadManualSegmentation(); // subir inmediatamente
      }
    }
  }

  uploadManualSegmentation() {
    if (!this.manualFile || !this.patientId) return;

    this.loading = true;
    this.uploadService
      .uploadManualSegmentation(this.patientId, this.manualFile)
      .subscribe({
        next: () => {
          this.router.navigate(['/ai/diagnosis_view'], {
            queryParams: { patient_id: this.patientId },
          });
        },
        error: (err) => {
          console.error('Error al subir segmentación manual:', err);
          alert('Error al subir segmentación.');
          this.loading = false;
        },
      });
  }
}
