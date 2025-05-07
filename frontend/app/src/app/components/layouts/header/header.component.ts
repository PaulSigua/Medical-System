import { Component, HostListener } from '@angular/core';
import {
  Bell,
  Brain
} from 'lucide-angular';


@Component({
  selector: 'app-header',
  standalone: false,
  templateUrl: './header.component.html',
  styleUrl: './header.component.css',
})
export class HeaderComponent {
  icons = { Bell, Brain };

  showUserMenu = false;

  toggleUserMenu() {
    this.showUserMenu = !this.showUserMenu;
  }

  @HostListener('document:click', ['$event'])
  handleClickOutside(event: Event) {
    const target = event.target as HTMLElement;
    const clickedInside = target.closest('.relative');
    if (!clickedInside) {
      this.showUserMenu = false;
    }
  }

}
