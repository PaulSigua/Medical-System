import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment.development';
import { HttpClient } from '@angular/common/http';
import { Patients } from '../../models/models';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PatientService {

  private apiUrl = environment.API_URL;

  constructor(
    private http: HttpClient
  ) {}

  registerPatient(data: Patients): Observable<any> {
    return this.http.post(`${this.apiUrl}/patients/register`, data)
  }

  getMyPatients(): Observable<Patients[]> {
    return this.http.get<Patients[]>(`${this.apiUrl}/patients/me`);
  }
}
