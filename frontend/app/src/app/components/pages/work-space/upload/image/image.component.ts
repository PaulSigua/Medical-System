import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Upload } from 'lucide-angular';
import { PatientService } from '../../../../../services/patients/patient.service';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-image',
  standalone: false,
  templateUrl: './image.component.html',
  styleUrl: './image.component.css',
})
export class ImageComponent implements OnInit {
  icons = { Upload };
  errorMessage = '';
  patient_id = '';
  selectedFiles: File[] = [];
  fileSelected: boolean = false;
  archivosInfo: { nombre: string; tamano: string }[] = [];
  showUploadZone: boolean = true;
  isLoading: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private patientSer: PatientService,
    private toastr: ToastrService
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      this.patient_id = params['patient_id'] || '';
    });
  }

  onFileChange(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (!input.files || input.files.length === 0) {
      this.toastr.error('No se seleccionaron archivos', 'Error');
      return;
    }
    this.selectedFiles = Array.from(input.files).filter((f) =>
      f.name.endsWith('.nii.gz')
    );
    if (this.selectedFiles.length === 0) {
      this.toastr.warning('Selecciona archivos .nii.gz', 'Advertencia');
      return;
    }
    this.uploadFiles();
  }

  private uploadFiles(): void {
    this.isLoading = true;
    const formData = new FormData();
    this.selectedFiles.forEach((file) => formData.append('files', file));
    formData.append('patient_id', this.patient_id);

    this.patientSer.uploadFiles(formData).subscribe({
      next: () => {
        this.toastr.success('Archivos subidos correctamente', 'Éxito');
        // Redirigir a Visualization pasando patient_id
        this.router.navigate(['/upload/visualization'], {
          queryParams: { patient_id: this.patient_id },
        });this.isLoading = false;
      },
      error: (err) => {
        console.error('Error subiendo archivos:', err);
        this.toastr.error('Error subiendo los archivos', 'Error');
        this.isLoading = false;
      },
    });
  }
}
