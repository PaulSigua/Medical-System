import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-password',
  standalone: false,
  templateUrl: './password.component.html',
  styleUrl: './password.component.css',
})
export class PasswordComponent {
  passForm!: FormGroup;

  showSuccess = false;

  constructor(private fb: FormBuilder) {
    this.passForm = this.fb.group({
      password: ['', Validators.required],
      newPassword: ['', Validators.required],
      confirmPassword: ['', Validators.required]
    });
  }

  passwordsMatch(group: FormGroup) {
    const pass = group.get('password')?.value;
    const confirm = group.get('confirmPassword')?.value;
    return pass === confirm ? null : { notMatching: true };
  }

  onSubmit() {
    if (this.passForm.valid) {
      console.log('Signup', this.passForm.value);
      // TODO: invocar servicio de registro
    }
  }

  showCurrentPassword = false;
  showPassword = false;
  showConfirmPassword = false;

  toggleRecurrentPassword() {
    this.showCurrentPassword = !this.showCurrentPassword;
  }

  togglePassword() {
    this.showPassword = !this.showPassword;
  }

  toggleConfirmPassword() {
    this.showConfirmPassword = !this.showConfirmPassword;
  }

  guardarCambios() {
    // Aquí iría tu lógica para guardar los cambios
    this.showSuccess = true;

    setTimeout(() => {
      this.showSuccess = false;
    }, 5000);
  }
}
