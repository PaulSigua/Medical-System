import { Component } from '@angular/core';
import { BarChart2, Brain, FileText, HelpCircle, Home, Settings, Upload, Users } from 'lucide-angular';
import { InfoPage } from '../../../../models/InfoPage';

@Component({
  selector: 'app-sidenav-ws',
  standalone: false,
  templateUrl: './sidenav.component.html',
  styleUrl: './sidenav.component.css'
})
export class SidenavComponent {

  info: InfoPage = new InfoPage();
  
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
