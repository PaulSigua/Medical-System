import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LoaderService {

  // Sujeto para manejar el estado de carga (true: cargando, false: inactivo)
  private isLoadingSubject = new BehaviorSubject<boolean>(false);

  // Observable que emite el estado de carga
  isLoading$ = this.isLoadingSubject.asObservable();

  // Activa el estado de carga.
  show(): void {
    this.isLoadingSubject.next(true);
  }

  // Desactiva el estado de carga.
  hide(): void {
    this.isLoadingSubject.next(false);
  }
}
