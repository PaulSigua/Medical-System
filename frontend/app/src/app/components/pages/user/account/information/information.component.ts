import { Component } from '@angular/core';
import { User } from 'lucide-angular';
import { InfoService } from '../../../../../services/user/info.service';
import { Patients, UpdateUser, Users } from '../../../../../models/models';
import { FormBuilder, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-information',
  standalone: false,
  templateUrl: './information.component.html',
  styleUrl: './information.component.css',
})
export class InformationComponent {
  icons = {
    User,
  };

  showSuccess = false;

  user!: Users;
  updateUser!: UpdateUser;
  patients: Patients[] = [];

  form!: FormGroup;
  isEditable = false;

  constructor(private userService: InfoService, private fb: FormBuilder) {}

  ngOnInit(): void {
    this.form = this.fb.group({
      name: [{ value: '', disabled: true }],
      last_name: [{ value: '', disabled: true }],
      phone: [{ value: '', disabled: true }],
      specialty: [{ value: '', disabled: true }],
    });

    this.userService.getCurrentUser().subscribe((data) => {
      this.form.patchValue(data);
      this.user = data;
      console.log(data);
    });
  }

  guardarCambios(): void {
    if (this.form.valid) {
      const updatedUser = this.form.getRawValue();
      if (this.user.id !== undefined) {
        console.log('Datos a guardar:', updatedUser);
        this.userService
          .updateCurrentUser(this.user.id, updatedUser)
          .subscribe({
            next: (updated) => {
              this.user = updated; // Actualizamos el modelo local con los nuevos datos
              this.form.patchValue(updated); // Refrescamos el form con datos "seguros"
              this.form.disable(); // Deshabilitamos el formulario
              this.isEditable = false; // Ocultamos el botón de guardar
              this.showSuccess = true; // Mostramos alerta temporal

              setTimeout(() => {
                this.showSuccess = false;
              }, 3000);
            },
            error: (err) => {
              console.error('Error actualizando usuario', err);
            },
          });
      } else {
        console.error('User ID is undefined. Cannot update user.');
      }
    }
  }

  toggleEdit(): void {
    if (this.isEditable) {
      // Si se cancela, restaurar valores originales
      this.form.patchValue(this.user);
      this.form.disable();
    } else {
      this.form.enable();
    }

    this.isEditable = !this.isEditable;
  }
}
