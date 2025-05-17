import { Component } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-password',
  standalone: false,
  templateUrl: './password.component.html',
  styleUrl: './password.component.css'
})
export class PasswordComponent {
  signupForm!: FormGroup;

  showSuccess = false;

  constructor(private fb: FormBuilder) {}
  
  passwordsMatch(group: FormGroup) {
    const pass = group.get('password')?.value;
    const confirm = group.get('confirmPassword')?.value;
    return pass === confirm ? null : { notMatching: true };
  }

  onSubmit() {
    if (this.signupForm.valid) {
      console.log('Signup', this.signupForm.value);
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
