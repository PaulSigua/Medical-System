import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment.development';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { finalize, Observable } from 'rxjs';
import { DiagnosticForm } from '../../models/diagnostics';

@Injectable({
  providedIn: 'root',
})
export class AiService {
  private apiUrl = environment.API_URL;

  constructor(private http: HttpClient) {}

  segmentPatient(
    uploadFolderId: string,
    framework = 'nnunet'
  ): Observable<{
    segmentation_url: string;
    summary_image_url: string;
    class_distribution_url: string;
    metrics: any;
    explanation: string;
  }> {
    const formData = new FormData();
    formData.append('upload_folder_id', uploadFolderId);
    formData.append('framework', framework);

    return this.http.post<{
      segmentation_url: string;
      summary_image_url: string;
      class_distribution_url: string;
      metrics: any;
      explanation: string;
    }>(`${this.apiUrl}/ai/segmentation`, formData);
  }

  saveDiagnostic(form: DiagnosticForm) {
    return this.http.post(`${this.apiUrl}/diagnostic/save`, form);
  }

  generateComparisonByPatient(patientId: string) {
    return this.http.get<any>(`${this.apiUrl}/ai/comparison_by_patient_id`, {
      params: { patient_id: patientId },
    });
  }
}
