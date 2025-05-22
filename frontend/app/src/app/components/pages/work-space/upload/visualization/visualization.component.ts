import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { GraphType } from '../../../../../services/patients/patient.service';

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

  graphOptions: { value: GraphType; viewValue: string }[] = [
    { value: 'graph6', viewValue: 'Visualización Interactiva de Modalidades' },
    { value: 'graph3D', viewValue: 'Visualización Cerebral 3D' },
  ];

  selectedGraph: GraphType = 'graph6';

  prediccion_clasificacion: string = '';

  constructor(private route: ActivatedRoute, private router: Router) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      this.patient_id = params['patient_id'] || '';
    });
  }

  sendForm() {
    if (this.diagnosticSelected && this.observations) {
      // Aquí puedes manejar el envío del formulario
      console.log('Diagnóstico seleccionado:', this.diagnosticSelected);
      console.log('observations:', this.observations);
      // Redirigir a otra página o realizar alguna acción adicional
      this.router.navigate(['/upload/image']); // Cambia '/next-page' por la ruta deseada
    }
  }
}
