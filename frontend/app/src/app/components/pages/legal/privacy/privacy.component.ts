import { Component } from '@angular/core';
import { ArrowLeft, Database, Eye, Lock, Shield } from 'lucide-angular';

@Component({
  selector: 'app-privacy',
  standalone: false,
  templateUrl: './privacy.component.html',
  styleUrl: './privacy.component.css'
})
export class PrivacyComponent {

  icons = {
    Shield,
    Lock,
    Eye,
    Database,
    ArrowLeft
  }
}
