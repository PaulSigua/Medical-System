import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment.development';
import { HttpClient } from '@angular/common/http';
import { Patients } from '../../models/models';
import { finalize, map, Observable } from 'rxjs';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

export type GraphType = 'graph6' | 'graph3D';

@Injectable({
  providedIn: 'root',
})
export class PatientService {
  private apiUrl = environment.API_URL;

  constructor(
    private http: HttpClient,
    private sanitizer: DomSanitizer
  ) {}

  /**
   * Registra un nuevo paciente.1
   * @param {Patients} data - Datos del paciente.
   * @returns {Observable<any>} Respuesta del servidor.
   */
  registerPatient(data: Patients): Observable<any> {
    return this.http.post(`${this.apiUrl}/patients/register`, data);
  }

  /**
   * Obtiene la lista de pacientes del usuario actual.
   * @returns {Observable<Patients[]>} Lista de pacientes.
   */
  getMyPatients(): Observable<Patients[]> {
    return this.http.get<Patients[]>(`${this.apiUrl}/patients/me`);
  }

  /**
   * Eliminar pacientes
   * 
   */
  deletePatient(patient_id: string): Observable<any> {
    console.log(`service delete patient ${[patient_id]}`)
    return this.http.delete<any>(`${this.apiUrl}/patients/delete/${patient_id}`)
  }

}
