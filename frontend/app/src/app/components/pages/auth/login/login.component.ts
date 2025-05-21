import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../../../services/auth/auth.service';

@Component({
  selector: 'app-login',
  standalone: false,
  templateUrl: './login.component.html',
  styleUrl: './login.component.css',
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup;
  showPassword = false;

  errorMessage: string | null = null;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    this.loginForm = this.fb.group({
      username: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required],
      // rememberSesion: [false, Validators.requiredTrue],
    });
    console.log('Credenciales: ', this.loginForm);
  }

  ngOnInit(): void {
    this.loginForm = this.fb.group({
      username: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required],
    });
    this.loginForm.valueChanges.subscribe(() => {
      if (this.loginForm.valid) {
        this.errorMessage = null;
      }
    });
  }

  togglePassword() {
    this.showPassword = !this.showPassword;
  }

  login() {
    this.errorMessage = null;
    this.loginForm.markAsUntouched();

    const controls = this.loginForm.controls;

    if (controls?.['username'].invalid || controls?.['password'].invalid) {
      this.errorMessage = 'Por favor complete todos los campos requeridos';
      return;
    }

    this.authService.login(this.loginForm.value).subscribe({
      next: (res) => {
        console.log('Inicio de sesion exitoso');
        this.authService.saveToken(res.access_token);
        this.router.navigate(['/work-space']); // Ruta protegida
        this.loginForm.reset();
      },
      error: (err) => {
      console.error('Login error', err);

        switch (err.status) {
          case 404:
            this.errorMessage = 'El usuario no existe.';
            break;
          case 401:
            this.errorMessage = 'Contraseña incorrecta.';
            break;
          default:
            this.errorMessage = 'Ocurrió un error. Intenta nuevamente.';
            break;
        }
        this.loginForm.reset()
      },
    });
  }
}
