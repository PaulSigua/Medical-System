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
    if (this.authSer.getToken()) return true;

    this.router.navigate(['/auth/login']);
    return false;
  }
}
