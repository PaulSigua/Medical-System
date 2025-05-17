import { Component } from '@angular/core';
import { User } from 'lucide-angular';
import { InfoService } from '../../../../../services/user/info.service';
import { Patients, Users } from '../../../../../models/models';
import { PatientService } from '../../../../../services/patients/patient.service';

@Component({
  selector: 'app-information',
  standalone: false,
  templateUrl: './information.component.html',
  styleUrl: './information.component.css'
})
export class InformationComponent {

  icons = {
    User
  };

  showSuccess = false;

  user!: Users;
  patients: Patients[] = [];

  constructor(
    private userService: InfoService,
  ) {}

  guardarCambios() {
    this.showSuccess = true;

    setTimeout(() => {
      this.showSuccess = false;
    }, 5000);
  }

  ngOnInit(): void {
    this.userService.getCurrentUser().subscribe((data) => {
      this.user = data;
      console.log(data)
    });
  }
}
