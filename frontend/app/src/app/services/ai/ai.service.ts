import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment.development';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { finalize, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AiService {
  private apiUrl = environment.API_URL;

  constructor(private http: HttpClient) {}

  detectionAI(patientId: string): Observable<any> {
    const requestBody = { patient_id: patientId };

    return this.http.post<any>(`${this.apiUrl}/ai/detection`, requestBody);
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
