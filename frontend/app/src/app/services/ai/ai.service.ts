import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment.development';
import { LoaderService } from '../upload/loader.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { finalize, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class IaService {
  private apiUrl = environment.API_URL;

  constructor(private loaderService: LoaderService, private http: HttpClient) {}

  detectionAI(patientId: string): Observable<any> {
    const requestBody = { patient_id: patientId };

    return this.http.post<any>(`${this.apiUrl}/ai/detection-ai`, requestBody);
  }

  /**
   * Realiza una predicción basada en IA para un paciente.
   *
   * @param {string} patientId - ID del paciente.
   * @returns {Observable<any>} Observable con la respuesta del servidor.
   */
  predictAI(patientId: string): Observable<any> {
    this.loaderService.show();
    return this.http
      .post<any>(
        `${this.apiUrl}/ai/predict-ai`,
        { patient_id: patientId },
        { withCredentials: true }
      )
      .pipe(finalize(() => this.loaderService.hide()));
  }

  /**
   * Genera una predicción basada en IA para un paciente.
   *
   * @param {string} patientId - ID del paciente.
   * @returns {Observable<any>} Observable con la respuesta del servidor.
   */
  generateAI(patientId: string): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });

    this.loaderService.show();
    return this.http
      .post<any>(
        `${this.apiUrl}/ai/predict-ia`,
        { patient_id: patientId },
        { headers, withCredentials: true }
      )
      .pipe(finalize(() => this.loaderService.hide()));
  }
}
