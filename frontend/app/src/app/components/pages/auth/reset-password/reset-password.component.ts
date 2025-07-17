import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../../../../services/auth/auth.service';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-reset-password',
  standalone: false,
  templateUrl: './reset-password.component.html',
  styleUrl: './reset-password.component.css',
})
export class ResetPasswordComponent {
  form: FormGroup;
  message: string | null = null;
  error: string | null = null;
  loading = false;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.form = this.fb.group({
      token: ['', Validators.required],
      new_password: ['', [Validators.required, Validators.minLength(6)]],
      confirm_password: ['', Validators.required],
    }, {
      validators: (group: FormGroup) => {
        const pass = group.get('new_password')?.value;
        const confirm = group.get('confirm_password')?.value;
        return pass === confirm ? null : { passwordMismatch: true };
      }
    });

    // Obtener el token desde la URL
    this.route.queryParams.subscribe((params) => {
      const token = params['token'];
      if (token) {
        this.form.patchValue({ token });
      }
    });
  }

  resetPassword() {
    this.error = null;

    if (this.form.invalid) {
      this.error = 'Verifica que todos los campos sean válidos';
      return;
    }

    this.loading = true;

    const { token, new_password } = this.form.value;
    this.authService.resetPassword({ token, new_password }).subscribe({
      next: () => {
        this.message = 'Contraseña actualizada con éxito. Redirigiendo...';
        setTimeout(() => this.router.navigate(['/auth/login']), 3000);
      },
      error: (err) => {
        this.loading = false;
        if (err.status === 400) {
          this.error = 'El enlace es inválido o ha expirado.';
        } else {
          this.error = 'Error al cambiar la contraseña. Intenta nuevamente.';
        }
      }
    });
  }
}
