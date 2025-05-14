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
export class LoginComponent{
  
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
      agreeTerms: [false],
    });
    console.log('Credenciales: ', this.loginForm)
  }

  togglePassword() { 
    this.showPassword = !this.showPassword;
  }

  login() {
    if (this.loginForm.invalid) {
      this.loginForm.markAllAsTouched();
      this.errorMessage = 'Por favor, completa todos los campos correctamente.';
      return;
    }
    
    this.errorMessage = null;

    this.authService.login(this.loginForm.value).subscribe({
      next: (res) => {
        this.authService.saveToken(res.access_token);
        this.router.navigate(['/work-space']); // Ruta protegida
      },
      error: (err) => {
        console.error('Login error', err);
        this.errorMessage = 'Credenciales incorrectas. Intenta nuevamente.';
      },
    });
  }

}