import { Component } from '@angular/core';
import { BarChart2, Brain, FileText, HelpCircle, Home, Settings, Upload, Users } from 'lucide-angular';

@Component({
  selector: 'app-sidenav-ws',
  standalone: false,
  templateUrl: './sidenav.component.html',
  styleUrl: './sidenav.component.css'
})
export class SidenavComponent {

  icons = {
    Home,
    Brain,
    Upload,
    BarChart2,
    FileText,
    Users,
    Settings,
    HelpCircle
  };
}
