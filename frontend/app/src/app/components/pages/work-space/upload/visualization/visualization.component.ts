import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import {
  GraphType,
  PatientService,
} from '../../../../../services/patients/patient.service';
import { SafeResourceUrl } from '@angular/platform-browser';

@Component({
  selector: 'app-visualization',
  standalone: false,
  templateUrl: './visualization.component.html',
  styleUrl: './visualization.component.css',
})
export class VisualizationComponent {
  diagnosticSelected: string = '';
  observations: string = '';

  patient_id = '';

  graphUrl?: SafeResourceUrl;

  graphOptions: { value: GraphType; viewValue: string }[] = [
    { value: 'graph6', viewValue: 'Visualización Interactiva de Modalidades' },
    { value: 'graph3D', viewValue: 'Visualización Cerebral 3D' },
  ];

  selectedGraph: GraphType = 'graph6';

  prediccion_clasificacion: string = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private patientService: PatientService
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      this.patient_id = params['patient_id'] || '';
      if (this.patient_id) {
        this.loadGraph(); // Cargar el gráfico por defecto
      }
    });
  }
  
  loadGraph() {
    if (!this.patient_id || !this.selectedGraph) return;
    this.patientService
      .fetchGraph(this.patient_id, this.selectedGraph)
      .subscribe({
        next: (url) => {
          this.graphUrl = url;
        },
        error: (err) => {
          console.error('Error al cargar gráfica:', err);
        },
      });
  }
  
  sendForm() {
    if (this.diagnosticSelected && this.observations) {
      console.log('Diagnóstico seleccionado:', this.diagnosticSelected);
      console.log('observations:', this.observations);
      this.router.navigate(['/work-space/patients']);
    }
  }
}
