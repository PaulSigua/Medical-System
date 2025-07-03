import { Component, OnInit } from '@angular/core';
import {
  AbstractControl,
  AsyncValidatorFn,
  FormBuilder,
  FormGroup,
  Validators,
} from '@angular/forms';
import { catchError, debounceTime, map, of, switchMap } from 'rxjs';
import { AuthService } from '../../../../services/auth/auth.service';
import { Users } from '../../../../models/models';
import { InfoPage } from '../../../../models/InfoPage';

export function usernameTakenValidator(
  authService: AuthService
): AsyncValidatorFn {
  return (ctrl: AbstractControl) => {
    if (!ctrl.value) return of(null);
    return of(ctrl.value).pipe(
      debounceTime(300),
      switchMap((username) =>
        authService.checkUsername(username).pipe(
          map((exists) => (exists ? { usernameTaken: true } : null)),
          catchError(() => of(null))
        )
      )
    );
  };
}

@Component({
  selector: 'app-signin',
  standalone: false,
  templateUrl: './signin.component.html',
  styleUrl: './signin.component.css',
})
export class SigninComponent implements OnInit {
  info: InfoPage = new InfoPage();
  signupForm!: FormGroup;

  showPassword = false;
  showConfirmPassword = false;

  errorMessage: string | null = null;
  succesfullMessage: string | null = null;

  user: Users = new Users();

  constructor(private fb: FormBuilder, private authService: AuthService) {
    this.signupForm = this.fb.group(
      {
        name: ['', Validators.required],
        last_name: ['', Validators.required],
        username: [
          '',
          [Validators.required, Validators.email],
          [usernameTakenValidator(this.authService)],
        ],
        password: ['', [Validators.required, Validators.minLength(12)]],
        confirmPassword: ['', [Validators.required]],
        agree_terms: [false, Validators.requiredTrue],
      },
      { validators: this.passwordsMatch }
    );
  }

  ngOnInit(): void {
    this.signupForm = this.fb.group(
      {
        name: ['', Validators.required],
        last_name: ['', Validators.required],
        username: [
          '',
          [Validators.required, Validators.email],
          [usernameTakenValidator(this.authService)],
        ],
        password: ['', [Validators.required]],
        confirmPassword: ['', Validators.required],
        agree_terms: [false, Validators.requiredTrue],
      },
      { validators: this.passwordsMatch }
    );

    this.signupForm.valueChanges.subscribe(() => {
      if (this.signupForm.valid) {
        this.errorMessage = null;
      }
    });
  }

  passwordsMatch(group: FormGroup) {
    const pass = group.get('password')?.value;
    const confirm = group.get('confirmPassword')?.value;
    return pass === confirm ? null : { notMatching: true };
  }

  togglePassword() {
    this.showPassword = !this.showPassword;
  }

  toggleConfirmPassword() {
    this.showConfirmPassword = !this.showConfirmPassword;
  }

  validatePassword() {
    const password = this.signupForm.get('password')?.value;
    const confirmpass = this.signupForm.get('confirmPassword')?.value;
    if (password !== confirmpass) {
      // console.log('Contrasenias validadas: ', password, '-', confirmpass);
      return false;
    }
    return true;
  }

  signIn() {
    this.errorMessage = null;
    this.signupForm.markAllAsTouched();

    const controls = this.signupForm.controls;

    if (
      controls?.['name'].invalid ||
      controls?.['last_name'].invalid ||
      controls?.['username'].invalid ||
      controls?.['password'].invalid ||
      controls?.['confirmPassword'].invalid
    ) {
      this.errorMessage = 'Por favor completa todos los campos requeridos.';
      return;
    }

    if (this.signupForm.errors?.['notMatching']) {
      this.errorMessage = 'Las contraseñas no coinciden.';
      return;
    }

    if (!controls?.['agree_terms'].value) {
      this.errorMessage = 'Debes aceptar los términos y condiciones.';
      return;
    }

    this.authService.register(this.signupForm.value).subscribe({
      next: () => {
        console.log('Usuario registrado con éxito');
        this.succesfullMessage =
          'Cuenta creada con éxito, por favor inicie sesión';
        this.signupForm.reset();
      },
      error: (err) => {
        console.error('Error en el registro: ', err);
        this.errorMessage =
          'No se pudo completar el registro. Intente nuevamente.';
        if (err.status === 409) {
          this.errorMessage = 'Ya existe un usuario con ese correo.';
        } else {
          this.errorMessage = 'Error al registrarse. Intente nuevamente.';
        }
      },
    });
  }
}