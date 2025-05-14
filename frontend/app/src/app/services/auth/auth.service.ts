import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment.development';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private apiUrl = environment.API_URL;

  constructor(private http: HttpClient) {}

  login(credentials: { username: string; password: string }): Observable<any> {
    return this.http.post(`${this.apiUrl}/auth/login`, credentials);
  }

  register(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/auth/register`, data);
  }

  logout(): void {
    localStorage.removeItem('access_token');
  }

  saveToken(token: string): void {
    localStorage.setItem('access_token', token);
  }

  getToken(): string | null {
    return localStorage.getItem('access_token');
  }

  isLoggedIn(): boolean {
    return !!localStorage.getItem('access_token');
  }
}
