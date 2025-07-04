import { Component, OnInit } from '@angular/core';
import { AbstractControl, FormBuilder, Validators } from '@angular/forms';
import {
  Brain,
  ClipboardPlusIcon,
  NotebookPen,
  NotebookPenIcon,
  Search,
  Trash2Icon,
} from 'lucide-angular';
import { PatientService } from '../../../../services/patients/patient.service';
import { Patients } from '../../../../models/models';
import { debounceTime, firstValueFrom } from 'rxjs';
import { Router } from '@angular/router';
import { AiService } from '../../../../services/ai/ai.service';

@Component({
  selector: 'app-patients',
  standalone: false,
  templateUrl: './patients.component.html',
  styleUrl: './patients.component.css',
})
export class PatientsComponent implements OnInit {
  icons = { Search, ClipboardPlusIcon, Brain, NotebookPenIcon, Trash2Icon };

  modalOpen = false;

  patients: Patients[] = [];
  filteredPatients: Patients[] = [];

  addPatientForm!: ReturnType<FormBuilder['group']>;
  searchPatientForm!: ReturnType<FormBuilder['group']>;

  public validator: boolean | undefined;

  showAlert = false;
  alertType: 'success' | 'error' | 'warning' = 'success';
  alertMessage = '';
  selectedPatientId: string | null = null;

  // cuando quieras disparar:
  // this.alertType    = 'success';
  // this.alertMessage = 'Paciente guardado correctamente.';
  // this.showAlert    = true;
  isLoading: boolean = false;

  constructor(
    private fb: FormBuilder,
    private patientService: PatientService,
    private iaServide: AiService,
    private router: Router
  ) {}

  private initForms(): void {
    this.addPatientForm = this.fb.group({
      patient_id: [
        '',
        [
          Validators.required,
          Validators.pattern(/^\d{10}$/),
          this.validadorDeCedula.bind(this),
        ],
      ],
      numero_historia_clinica: [
        '',
        [Validators.required, Validators.pattern(/^[0-1]$/)],
      ],
    });

    this.searchPatientForm = this.fb.group({
      searchPatientId: ['', [Validators.pattern(/^\d{0,10}$/)]],
    });
  }

  ngOnInit(): void {
    this.initForms();
    this.getPatients();

    this.searchPatientForm
      .get('searchPatientId')
      ?.valueChanges.pipe(debounceTime(300))
      .subscribe(() => {
        this.searchPatients();
      });
  }

  // 🔄 Función genérica para sanitizar input numérico
  sanitizeNumericInput(
    control: AbstractControl | null,
    maxLength: number,
    event: Event
  ) {
    const input = event.target as HTMLInputElement;
    const cleaned = input.value.replace(/\D/g, '').slice(0, maxLength);
    control?.setValue(cleaned, { emitEvent: false });
  }

  onCedulaInput(event: Event): void {
    this.sanitizeNumericInput(this.addPatientForm.get('patient_id'), 10, event);
  }

  onHistoryCli(event: Event): void {
    this.sanitizeNumericInput(
      this.addPatientForm.get('numero_historia_clinica'),
      1,
      event
    );
  }

  searchCedulaInput(event: Event): void {
    this.sanitizeNumericInput(
      this.searchPatientForm.get('searchPatientId'),
      10,
      event
    );
    this.searchPatients();
  }

  validadorDeCedula(control: AbstractControl) {
    const id = control.value;
    if (typeof id !== 'string' || id.length !== 10)
      return { cedulaInvalida: true };

    const thirdDigit = parseInt(id[2]);
    if (thirdDigit >= 6) return { cedulaInvalida: true };

    const coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2];
    const verificador = parseInt(id[9]);

    let suma = 0;
    for (let i = 0; i < 9; i++) {
      let valor = parseInt(id[i]) * coeficientes[i];
      if (valor >= 10) valor -= 9;
      suma += valor;
    }

    const decenaSuperior = Math.ceil(suma / 10) * 10;
    const digitoVerificador = decenaSuperior - suma;

    if (
      (digitoVerificador === 10 && verificador === 0) ||
      digitoVerificador === verificador
    ) {
      return null; // válido
    }

    return { cedulaInvalida: true };
  }

  registerPatients() {
    console.log('Paciente:', this.addPatientForm.value);
    this.patientService.registerPatient(this.addPatientForm.value).subscribe({
      next: () => {
        this.alertType = 'success';
        this.alertMessage = 'Paciente guardado correctamente.';
        this.showAlert = true;
        this.modalOpen = false;
        this.getPatients();
      },
      error: (err) => {
        if (err.status == 409) {
          this.alertType = 'error';
          this.alertMessage = 'El paciente ya existe.';
          this.showAlert = true;
        } else {
          this.alertType = 'error';
          this.alertMessage = 'No se pudo guardar el paciente.';
          this.showAlert = true;
        }
      },
    });
  }

  searchPatients() {
    const searchValue =
      this.searchPatientForm.get('searchPatientId')?.value || '';
    this.filteredPatients = searchValue
      ? this.patients.filter((p) => p.patient_id?.includes(searchValue))
      : this.patients;
    if (this.filteredPatients.length <= 0) {
      this.alertType = 'error';
      this.alertMessage = 'No se encontro el paciente';
      this.showAlert = true;
    } else {
      this.alertType = 'success';
      this.alertMessage = 'El paciente si existe';
      this.showAlert = true;
    }
  }

  getPatients() {
    this.patientService.getMyPatients().subscribe((patients: Patients[]) => {
      this.patients = patients;
      this.filteredPatients = patients;
    });
  }

  eliminarDiagnostico(patient: Patients) {
    console.log('Eliminando paciente:', patient);
  }

  generateDiagnosis(patient_id: string) {
    try {
      this.isLoading = true;
      this.selectedPatientId = patient_id;
      this.router.navigate(['/upload'], {
        queryParams: { patient_id: patient_id },
      });
      console.log('Paciente seleccionado:', this.selectedPatientId);
      console.log('go');
    } catch (error) {
      console.log(
        'Ocurrio un error al generar el diagnostico por el medico, ',
        error
      );
      this.isLoading = false;
    }
    this.isLoading = false;
  }

  async generateAIDiagnosis(patient_id: string): Promise<void> {
    this.selectedPatientId = patient_id;
    this.isLoading = true;

    try {
      // 1) Mostrar alerta inicial de carga
      this.alertType = 'warning';
      this.alertMessage = 'Generando diagnóstico con IA…';
      this.showAlert = true;

      // 2) Detección general
      const detRes = await firstValueFrom(
        this.iaServide.detectionAI(patient_id)
      );
      const score = parseFloat(detRes?.message ?? '0');
      const detMsg = score >= 0.5 ? 'Cáncer Detectado' : 'No se detectó cáncer';

      // 3) Predicción detallada
      const pred = await firstValueFrom(this.iaServide.predictAI(patient_id));

      // 4) Redirigir como queryParams
      await this.router.navigate(['/ia'], {
        queryParams: {
          patient_id,
          html_url1: pred.html_url1,
          html_url2: pred.html_url2,
          html_url3: pred.html_url3,
          html_url4: pred.html_url4,
          html_url5: pred.html_url5,
          html_url6: pred.html_url6,
          detection_message: detMsg,
        },
      });
    } catch (err) {
      console.error('Error diagnóstico IA:', err);
      this.alertType = 'error';
      this.alertMessage = 'Error al generar el diagnóstico con IA.';
      this.showAlert = true;
    } finally {
      this.isLoading = false;
    }
  }

  uploadComparisonSegmentation(){
    this.router.navigate([('/work-space/upload/segmentation')])
  }

  deletePatient(id: string) {
    
  } 
}
