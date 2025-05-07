import { Component } from '@angular/core';
import {
  Home,
  Brain,
  Upload,
  BarChart2,
  FileText,
  Users,
  Settings,
  HelpCircle
} from 'lucide-angular';


@Component({
  selector: 'app-sidenav',
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
