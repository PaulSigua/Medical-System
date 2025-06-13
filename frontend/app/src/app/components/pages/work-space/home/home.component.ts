import { Component } from '@angular/core';
import { Brain, PersonStanding, User } from 'lucide-angular';

@Component({
  selector: 'app-home',
  standalone: false,
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {

  icons = {
    PersonStanding,
    Brain
  }
}
