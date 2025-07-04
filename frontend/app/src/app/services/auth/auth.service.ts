import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { map, Observable } from 'rxjs';
import { environment } from '../../../environments/environment.development';
import { Users } from '../../models/models';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root',
})

export class AuthService {
  private apiUrl = environment.API_URL;

  constructor(
    private http: HttpClient,
    private router: Router
  ) {}

/**
   * Inicia sesión con credenciales.
   * @param credentials - Nombre de usuario y contraseña.
   * @returns Observable con el token o error.
   */
  login(credentials: { username: string; password: string }): Observable<any> {
    return this.http.post(`${this.apiUrl}/auth/login`, credentials);
  }

  /**
   * Registra un nuevo usuario.
   * @param {Users} data - Datos del usuario.
   * @returns {Observable<any>} Respuesta del servidor.
   */
  register(data: Users): Observable<any> {
    return this.http.post(`${this.apiUrl}/auth/register`, data);
  }

  /**
   * Verifica si un nombre de usuario ya está en uso.
   * @param username - Nombre de usuario.
   * @returns Observable<boolean> indicando si ya existe.
   */
  checkUsername(username: string): Observable<boolean> {
    return this.http
      .get<{ exists: boolean }>(`${this.apiUrl}/auth/check-username`, {
        params: { username },
      })
      .pipe(map((res) => res.exists));
  }

  /**
   * Cierra sesión y redirige al login.
   */
  logout(): void {
    if (typeof window !== 'undefined' && localStorage) {
      localStorage.removeItem('access_token');
      this.router.navigate(['/auth/login']);
    }
  }

  /**
   * Guarda el token en localStorage.
   * @param token - Token JWT.
   */
  saveToken(token: string): void {
    if (typeof window !== 'undefined' && localStorage) {
      localStorage.setItem('access_token', token);
    }
  }

  /**
   * Recupera el token del localStorage.
   * @returns Token JWT o null.
   */
  getToken(): string | null {
    if (typeof window !== 'undefined' && localStorage) {
      return localStorage.getItem('access_token');
    }
    return null;
  }

  /**
   * Verifica si el usuario ha iniciado sesión.
   * @returns `true` si hay token, `false` si no.
   */
  isLoggedIn(): boolean {
    if (typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
      return !!localStorage.getItem('access_token');
    }
    return false;
  }
}
