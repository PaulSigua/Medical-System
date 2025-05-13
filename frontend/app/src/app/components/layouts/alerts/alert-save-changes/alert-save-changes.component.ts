import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-alert-save-changes',
  standalone: false,
  templateUrl: './alert-save-changes.component.html',
  styleUrl: './alert-save-changes.component.css'
})
export class AlertSaveChangesComponent {

  @Input() type: 'success' | 'error' | 'warning' = 'success';
  @Input() message = '';
  @Input() show = false;
}
