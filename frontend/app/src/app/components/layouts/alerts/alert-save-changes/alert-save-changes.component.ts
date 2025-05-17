import { Component, Input, Output, SimpleChanges, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-alert-save-changes',
  standalone: false,
  templateUrl: './alert-save-changes.component.html',
  styleUrl: './alert-save-changes.component.css'
})
export class AlertSaveChangesComponent {

  @Input() type: 'success' | 'error' | 'warning' = 'success';
  @Input() message: string = '';
  @Input() show: boolean = false;
  @Input() duration: number = 5000; // auto-dismiss in ms
  @Output() closed = new EventEmitter<void>();

  visible: boolean = false;

  ngOnChanges(changes: SimpleChanges) {
    if (changes['show'] && this.show) {
      this.visible = true;
      // auto dismiss
      setTimeout(() => {
        this.visible = false;
        this.closed.emit();
      }, this.duration);
    }
  }
}
