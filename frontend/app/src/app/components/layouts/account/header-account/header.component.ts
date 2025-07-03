import { Component } from '@angular/core';
import { ArrowLeft, ChevronDown, Home } from 'lucide-angular';
import { InfoPage } from '../../../../models/InfoPage';

@Component({
  selector: 'app-header-account',
  standalone: false,
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})
export class HeaderComponent {

  info: InfoPage = new InfoPage();

  icons = {
    ArrowLeft,
    Home,
    ChevronDown
  };
}
