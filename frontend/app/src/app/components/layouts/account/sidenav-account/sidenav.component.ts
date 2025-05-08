import { Component } from '@angular/core';
import { Settings, User } from 'lucide-angular';

@Component({
  selector: 'app-sidenav-account',
  standalone: false,
  templateUrl: './sidenav.component.html',
  styleUrl: './sidenav.component.css'
})
export class SidenavComponent {

  icons = {
    User,
    Settings
  };
}
