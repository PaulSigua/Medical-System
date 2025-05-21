import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment.development';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { UpdateUser, Users } from '../../models/models';

@Injectable({
  providedIn: 'root'
})
export class InfoService {

  private apiUrl = environment.API_URL;

  constructor(
    private http: HttpClient
  ) {}

  getCurrentUser(): Observable<Users> {
    return this.http.get<Users>(`${this.apiUrl}/users/me`);
  }

  updateCurrentUser(id: number, data: UpdateUser): Observable<UpdateUser> {
    return this.http.put<UpdateUser>(`${this.apiUrl}/users/${id}`, data)
  }
}
