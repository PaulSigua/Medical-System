import { Component, HostListener } from '@angular/core';
import { Bell, X } from 'lucide-angular';

@Component({
  selector: 'app-notifications',
  standalone: false,
  templateUrl: './notifications.component.html',
  styleUrl: './notifications.component.css'
})
export class NotificationsComponent {

  icons = {
    Bell,
    X,
  };


  isOpen = false;

  toggle() {
    this.isOpen = !this.isOpen;
  }

  close() {
    this.isOpen = false;
  }

  // Cierra el dropdown si el usuario hace click fuera
  @HostListener('document:click', ['$event.target'])
  onClickOutside(target: HTMLElement) {
    const clickedInside = target.closest('app-notifications');
    if (!clickedInside) {
      this.isOpen = false;
    }
  }
}
