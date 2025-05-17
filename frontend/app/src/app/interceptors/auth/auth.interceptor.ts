import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
  HttpErrorResponse
} from '@angular/common/http';
import { catchError, Observable, throwError } from 'rxjs';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth/auth.service';
import { NotificationService } from '../../services/token/notification.service';

@Injectable()
export class TokenInterceptor implements HttpInterceptor {

  constructor(
    private router: Router,
    private authService: AuthService,
    private notificationService: NotificationService // puedes usar ngx-toastr o tu propio servicio
  ) {}

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const token = this.authService.getToken();

    if (token) {
      request = request.clone({
        setHeaders: {
          Authorization: `Bearer ${token}`
        }
      });
    }

    return next.handle(request).pipe(
      catchError((error: HttpErrorResponse) => {
        if (error.status === 401 && !request.url.includes('/auth/login')) {
          this.authService.logout();

          // Mostrar mensaje amigable
          this.notificationService.show(
            'Tu sesión ha expirado. Por favor, vuelve a iniciar sesión.',
            'Sesión finalizada',
            'warning'
          );

          // Redirigir al login
          this.router.navigate(['/auth/login']);
        }

        return throwError(() => error);
      })
    );
  }
}
