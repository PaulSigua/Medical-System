import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment.development';
import { HttpClient } from '@angular/common/http';
import { Patients } from '../../models/models';
import { finalize, Observable } from 'rxjs';
import { LoaderService } from '../upload/loader.service';
import { GraphResponse } from '../../models/patient';

@Injectable({
  providedIn: 'root'
})
export class PatientService {

  private apiUrl = environment.API_URL;

  constructor(
    private http: HttpClient,
    private loaderService: LoaderService
  ) {}

  /**
   * Registra un nuevo paciente.
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
   * Sube archivos al servidor.
   * @param {FormData} formData - Datos del formulario con archivos.
   * @returns {Observable<any>} Respuesta del servidor.
   */
  uploadFiles(formData: FormData): Observable<any> {
    this.loaderService.show();
    return this.http.post(`${this.apiUrl}/patients/upload/files`, formData, { withCredentials: true }).pipe(
      finalize(() => this.loaderService.hide())
    );
  }

    /**
   * Genera un gráfico de tipo 6 para un paciente.
   *
   * @param {string} patientId - ID del paciente.
   * @returns {Observable<any>} Observable con la respuesta del servidor.
   */
  predict6(patientId: string): Observable<GraphResponse> {
    this.loaderService.show();
    return this.http.post<GraphResponse>(
      `${this.apiUrl}/graphs/generate-graph6`,
      { patient_id: patientId },
      { withCredentials: true }
    ).pipe(
      finalize(() => this.loaderService.hide())
    );
  }
}
