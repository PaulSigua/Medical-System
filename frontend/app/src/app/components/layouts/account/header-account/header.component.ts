import { Component } from '@angular/core';
import { ArrowLeft, ChevronDown, Home } from 'lucide-angular';

@Component({
  selector: 'app-header-account',
  standalone: false,
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})
export class HeaderComponent {

  icons = {
    ArrowLeft,
    Home,
    ChevronDown
  };
}
