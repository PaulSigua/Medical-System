import { Component } from '@angular/core';
import { Router } from '@angular/router';


@Component({
  selector: 'app-visualization',
  standalone: false,
  templateUrl: './visualization.component.html',
  styleUrl: './visualization.component.css',
})
export class VisualizationComponent {
  diagnosticSelected: string = '';
  observations: string = '';

  constructor(private router: Router) { }

  sendForm() {
    if (this.diagnosticSelected && this.observations) {
      // Aquí puedes manejar el envío del formulario
      console.log('Diagnóstico seleccionado:', this.diagnosticSelected);
      console.log('observations:', this.observations);
      // Redirigir a otra página o realizar alguna acción adicional
      this.router.navigate(['/upload/image']) // Cambia '/next-page' por la ruta deseada
    }
  }
}
