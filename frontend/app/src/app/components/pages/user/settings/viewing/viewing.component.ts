import { Component } from '@angular/core';

@Component({
  selector: 'app-viewing',
  standalone: false,
  templateUrl: './viewing.component.html',
  styleUrl: './viewing.component.css'
})
export class ViewingComponent {

  showSuccess = false;

  guardarCambios() {
    // Aquí iría tu lógica para guardar los cambios
    this.showSuccess = true;

    setTimeout(() => {
      this.showSuccess = false;
    }, 5000);
  }
}
