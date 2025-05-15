import { Component } from '@angular/core';
import { Router } from '@angular/router';


@Component({
  selector: 'app-visualization',
  standalone: false,
  templateUrl: './visualization.component.html',
  styleUrl: './visualization.component.css',
})
export class VisualizationComponent {
  diagnosticoSeleccionado: string = '';
  observaciones: string = '';

  constructor(private router: Router) { }

  enviarFormulario() {
    if (this.diagnosticoSeleccionado && this.observaciones) {
      // Aquí puedes manejar el envío del formulario
      console.log('Diagnóstico seleccionado:', this.diagnosticoSeleccionado);
      console.log('Observaciones:', this.observaciones);
      // Redirigir a otra página o realizar alguna acción adicional
      this.router.navigate(['/upload/image']) // Cambia '/next-page' por la ruta deseada
    }
  }
}
