import { Component } from '@angular/core';
import { User } from 'lucide-angular';

@Component({
  selector: 'app-information',
  standalone: false,
  templateUrl: './information.component.html',
  styleUrl: './information.component.css'
})
export class InformationComponent {

  icons = {
    User
  };

  showSuccess = false;

  guardarCambios() {
    // Aquí iría tu lógica para guardar los cambios
    this.showSuccess = true;

    setTimeout(() => {
      this.showSuccess = false;
    }, 5000);
  }
}
