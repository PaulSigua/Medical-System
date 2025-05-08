import { Component } from '@angular/core';
import { ArrowLeft } from 'lucide-angular';

@Component({
  selector: 'app-settings',
  standalone: false,
  templateUrl: './settings.component.html',
  styleUrl: './settings.component.css'
})
export class SettingsComponent {

  icons = {
    ArrowLeft
  };
}
