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
}
