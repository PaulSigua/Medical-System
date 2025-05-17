import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class NotificationService {

  constructor() { }

  show(message: string, title: string, type: 'success' | 'error' | 'info' | 'warning') {
    alert(`${title}: ${message}`); // reemplaza esto con una mejor librería si quieres
  }
}
