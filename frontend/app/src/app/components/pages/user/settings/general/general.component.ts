import { Component } from '@angular/core';

@Component({
  selector: 'app-general',
  standalone: false,
  templateUrl: './general.component.html',
  styleUrl: './general.component.css'
})
export class GeneralComponent {

  showSuccess = false;

  guardarCambios() {
    // Aquí iría tu lógica para guardar los cambios
    this.showSuccess = true;

    setTimeout(() => {
      this.showSuccess = false;
    }, 5000);
  }
}
