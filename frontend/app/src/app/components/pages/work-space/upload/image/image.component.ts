import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { ActivatedRoute, Router } from '@angular/router';
import { Upload } from 'lucide-angular';
import { PatientService } from '../../../../../services/patients/patient.service';
import { ToastrService } from 'ngx-toastr';
import { Patients } from '../../../../../models/models';

@Component({
  selector: 'app-image',
  standalone: false,
  templateUrl: './image.component.html',
  styleUrl: './image.component.css',
})
export class ImageComponent implements OnInit{
  icons = {
    Upload,
  };

  errorMessage = false;

  selectedGraph: string = '';
  patient_id: string = '';

  patients: Patients[] = [];
  filteredPatients: Patients[] = [];
  selectedFiles: File[] = [];
  prediccion_clasificacion: string = '';
  isCollapsed: boolean = false;

  isGraph6Loaded: boolean = false;
  isGraph3DLoaded: boolean = false;
  htmlUrl6: SafeResourceUrl | null = null;
  htmlUrl3D: SafeResourceUrl | null = null;

  /** Opciones de gráficas disponibles */
  graphOptions = [
    { value: 'graph6', viewValue: 'Visualización Interactiva de Modalidades' },
    { value: 'graph3D', viewValue: 'Visualización Cerebral 3D' },
  ];

  constructor(
    private route: ActivatedRoute,
    private patientSer: PatientService,
    private sanitizer: DomSanitizer,
    private toastr: ToastrService // private detectionService: DetectionService
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      console.log('Query params:', params);
      this.patient_id = params['patient_id'];
      console.log('Paciente cargado en ngOnInit:', this.patient_id);
    });
  }

  getPatients() {
    this.patientSer.getMyPatients().subscribe((patients: Patients[]) => {
      this.patients = patients;
      this.filteredPatients = patients;
    });
  }

  onFileChange(event: Event): void {
    const input = event.target as HTMLInputElement;

    if (!input.files || input.files.length === 0) {
      alert('No se seleccionaron archivos.');
      return;
    }

    this.selectedFiles = Array.from(input.files).filter((file) =>
      file.name.endsWith('.nii.gz')
    );

    if (this.selectedFiles.length === 0) {
      this.toastr.warning(
        'Ninguno de los archivos seleccionados tiene formato .nii.gz'
      );
      return;
    }

    console.log('Archivos seleccionados:', this.selectedFiles);
    this.uploadFiles();
  }

  private uploadFiles(): void {
    if (this.selectedFiles.length === 0) {
      this.toastr.error('No se seleccionaron archivos.');
      console.warn('No has seleccionado archivos .nii.gz');
      return;
    }

    const formData = this.buildFormData(this.selectedFiles, this.patient_id);

    this.patientSer.uploadFiles(formData).subscribe({
      next: () => {
        this.toastr.success('Archivos subidos correctamente', 'Éxito');
        console.log(`Paciente cargafo: ${this.patient_id}`)
        this.loadGraphs(this.patient_id);
        // this.runClassification(this.patient_id);
      },
      error: (err) => {
        console.error('Error subiendo los archivos:', err);
        this.toastr.error('Error subiendo los archivos', 'Error');
      },
    });
  }

  private buildFormData(files: File[], patient_id: string): FormData {
    const formData = new FormData();
    files.forEach((file) => formData.append('files', file));
    formData.append('patient_id', patient_id);
    return formData;
  }

  private loadGraphs(patient_id: string): void {
    console.log(patient_id)
    this.patientSer.predict6(patient_id).subscribe({
      next: (response) => {
        if (response.html_url6 && response.html_url6) {
          this.htmlUrl6 = this.sanitizer.bypassSecurityTrustResourceUrl(
            response.html_url6
          );
          this.htmlUrl3D = this.sanitizer.bypassSecurityTrustResourceUrl(
            response.html_url6
          );
          this.isGraph6Loaded = true;
          this.isGraph3DLoaded = true;
        } else {
          this.toastr.warning(
            'No se pudieron cargar las gráficas: faltan URLs en la respuesta.',
            'Advertencia'
          );
          console.warn('Respuesta incompleta:', response);
        }
      },
      error: (err) => {
        console.error('Error al cargar gráficas:', err);
        this.toastr.error(
          'Error al obtener las gráficas del paciente.',
          'Error'
        );
      },
    });
  }
}