import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: false,
  templateUrl: './login.component.html',
  styleUrl: './login.component.css',
})
export class LoginComponent implements OnInit {
  // loginForm!: FormGroup; — ahora no da error porque TS sabe que se inicializa en ngOnInit
  loginForm!: FormGroup;

  constructor(
    private fb: FormBuilder,
    private router: Router,
  ) {}

  ngOnInit() {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required],
      agreeTerms: [false],
    });
  }

  onSubmit() {
    /* … */
  }

  showPassword = false;

  togglePassword() {
    this.showPassword = !this.showPassword;
  }

  goToWorkSpace() {
    this.router.navigate([('/work-space')]);
  }
  
}
