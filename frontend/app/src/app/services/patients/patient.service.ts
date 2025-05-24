import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment.development';
import { HttpClient } from '@angular/common/http';
import { Patients } from '../../models/models';
import { finalize, map, Observable } from 'rxjs';
import { LoaderService } from '../upload/loader.service';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

export type GraphType = 'graph6' | 'graph3D';

@Injectable({
  providedIn: 'root',
})
export class PatientService {
  private apiUrl = environment.API_URL;

  constructor(
    private http: HttpClient,
    private sanitizer: DomSanitizer,
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
    return this.http
      .post(`${this.apiUrl}/patients/upload/files`, formData, {
        withCredentials: true,
      })
      .pipe(finalize(() => this.loaderService.hide()));
  }

  /**
   * Genera un gráfico de tipo 6 para un paciente.
   *
   * @param {string} patientId - ID del paciente.
   * @returns {Observable<any>} Observable con la respuesta del servidor.
   */
  fetchGraph(patientId: string, type: GraphType): Observable<SafeResourceUrl> {
    const endpoint = type === 'graph6' ? 'generate-graph6' : 'generate-graph3D';
    this.loaderService.show();
    console.log('Llamando fetchGraph con tipo:', type);
    return this.http
      .post<{ html_url6?: string; html_url3D?: string }>(
        `${this.apiUrl}/graphs/${endpoint}`,
        { patient_id: patientId },
        { withCredentials: true }
      )
      .pipe(
        map((res) => {
          const raw = type === 'graph6' ? res.html_url6 : res.html_url3D;
          if (!raw) throw new Error('No URL recibida');
          // Usa la URL base sin /api
          const fullUrl = `${environment.BACKEND_URL}${raw}`;
          return this.sanitizer.bypassSecurityTrustResourceUrl(fullUrl);
        }),
        finalize(() => this.loaderService.hide())
      );
  }
}
