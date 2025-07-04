import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment.development';
import { LoaderService } from '../upload/loader.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { finalize, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AiService {
  private apiUrl = environment.API_URL;

  constructor(private loaderService: LoaderService, private http: HttpClient) {}

  detectionAI(patientId: string): Observable<any> {
    const requestBody = { patient_id: patientId };

    return this.http.post<any>(`${this.apiUrl}/ai/detection`, requestBody);
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
        `${this.apiUrl}/ai/prediction`,
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
        `${this.apiUrl}/ai/prediction`,
        { patient_id: patientId },
        { headers, withCredentials: true }
      )
      .pipe(finalize(() => this.loaderService.hide()));
  }

  segmentTumor(
    patientId: string,
    files: { T1c: File; T2W: File; T2F: File }
  ): Observable<{ segmentation_url: string }> {
    const formData = new FormData();
    formData.append('patient_id', patientId);
    formData.append('T1c', files.T1c);
    formData.append('T2W', files.T2W);
    formData.append('T2F', files.T2F);

    return this.http.post<{ segmentation_url: string }>(
      `${this.apiUrl}/ai/segmentation`,
      formData
    );
  }
}
