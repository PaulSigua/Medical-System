import { Component } from '@angular/core';
import { ArrowLeft, Key, User } from 'lucide-angular';

@Component({
  selector: 'app-account',
  standalone: false,
  templateUrl: './account.component.html',
  styleUrl: './account.component.css'
})
export class AccountComponent {

  icons = {
    User,
    Key,
    ArrowLeft
  }
}
