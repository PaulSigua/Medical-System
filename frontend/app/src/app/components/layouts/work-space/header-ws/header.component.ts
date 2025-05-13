import { Component, HostListener } from '@angular/core';
import { Bell, Brain, X } from 'lucide-angular';

@Component({
  selector: 'app-header-ws',
  standalone: false,
  templateUrl: './header.component.html',
  styleUrl: './header.component.css',
})
export class HeaderComponent {
  icons = { Bell, Brain, X };

  showUserMenu = false;
  showNotifications = false;

  notifications = [
    { text: 'Tienes un nuevo mensaje.', time: 'Hace 2 horas' },
    { text: 'Tu reporte está listo.', time: 'Hace 1 día' }
  ];

  toggleUserMenu() {
    this.showUserMenu = !this.showUserMenu;
    if (this.showUserMenu) this.showNotifications = false;
  }

  toggleNotifications() {
    this.showNotifications = !this.showNotifications;
    if (this.showNotifications) this.showUserMenu = false;
  }

  @HostListener('document:click', ['$event.target'])
  onClickOutside(target: HTMLElement) {
    if (!target.closest('header')) {
      this.showUserMenu = false;
      this.showNotifications = false;
    }
  }
}