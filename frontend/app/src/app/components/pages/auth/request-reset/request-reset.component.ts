import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../../../../services/auth/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-request-reset',
  standalone: false,
  templateUrl: './request-reset.component.html',
  styleUrl: './request-reset.component.css'
})
export class RequestResetComponent {
  form: FormGroup;
  token: string | null = null;
  error: string | null = null;
  loading = false;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    this.form = this.fb.group({
      username: ['', [Validators.required, Validators.email]],
    });
  }

  requestReset() {
    this.error = null;

    if (this.form.invalid) {
      this.error = 'Ingresa un correo válido';
      return;
    }

    this.loading = true;

    const username = this.form.value.username;
    this.authService.requestPasswordReset(username).subscribe({
      next: (res) => {
        const token = res.reset_token;
        this.router.navigate(['/auth/reset-password'], {
          queryParams: { token }
        });
      },
      error: (err) => {
        this.loading = false;
        if (err.status === 404) {
          this.error = 'No existe una cuenta con ese correo.';
        } else {
          this.error = 'Ocurrió un error. Intenta nuevamente.';
        }
      },
    });
  }
}

