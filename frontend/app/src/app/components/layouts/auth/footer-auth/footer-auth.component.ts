import { Component } from '@angular/core';
import { InfoPage } from '../../../../models/InfoPage';

@Component({
  selector: 'app-footer-auth',
  standalone: false,
  templateUrl: './footer-auth.component.html',
  styleUrl: './footer-auth.component.css'
})
export class FooterAuthComponent {

  info: InfoPage = new InfoPage();

  constructor() {
  }
}
