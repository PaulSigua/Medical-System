import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment.development';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class UploadService {
  private apiUrl = environment.API_URL;

  constructor(private http: HttpClient) {}

  uploadNiftiFiles(patientId: string, files: File[]): Observable<any> {
    const formData = new FormData();
    formData.append('patient_id', patientId);
    files.forEach((file) => formData.append('files', file));
    return this.http.post(`${this.apiUrl}/upload/nifti_files`, formData);
  }
}
