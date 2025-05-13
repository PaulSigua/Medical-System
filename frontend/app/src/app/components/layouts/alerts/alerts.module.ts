import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AlertSaveChangesComponent } from './alert-save-changes/alert-save-changes.component';
import { NotificationsComponent } from './notifications/notifications.component';
import { LucideAngularModule } from 'lucide-angular';



@NgModule({
  declarations: [
    AlertSaveChangesComponent,
    NotificationsComponent
  ],
  imports: [
    CommonModule,
    LucideAngularModule
  ],
  exports: [
    AlertSaveChangesComponent,
    NotificationsComponent
  ],
})
export class AlertsModule { }
