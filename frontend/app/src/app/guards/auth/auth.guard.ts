// auth.guard.ts
import { Injectable } from '@angular/core';
import {
  CanActivate,
  Router
} from '@angular/router';
import { AuthService } from '../../services/auth/auth.service';

@Injectable({ providedIn: 'root' })
export class AuthGuard implements CanActivate {
  constructor(private authSer: AuthService, private router: Router) {}

  canActivate(): boolean {
    const token = this.authSer.getToken();
    if (token) return true;

    // Esto evita parpadeos extraños y asegura navegación
    this.router.navigate(['/auth/login'], { replaceUrl: true });
    return false;
  }
}
