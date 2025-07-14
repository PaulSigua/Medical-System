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

  segmentPatient(uploadFolderId: string, framework = 'nnunet'): Observable<any> {
    const formData = new FormData();
    formData.append('upload_folder_id', uploadFolderId);
    formData.append('framework', framework);
    return this.http.post(`${this.apiUrl}/ai/segmentation`, formData);
  }
}
