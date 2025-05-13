import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AlertSaveChangesComponent } from './alert-save-changes/alert-save-changes.component';



@NgModule({
  declarations: [
    AlertSaveChangesComponent
  ],
  imports: [
    CommonModule
  ],
  exports: [
    AlertSaveChangesComponent
  ],
})
export class AlertsModule { }
