import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { VisualizationComponent } from './visualization/visualization.component';
import { WorkSpaceModule } from '../../../layouts/work-space/work-space.module';
import { RouterModule, Routes } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { UploadManualComponent } from './upload-manual/upload-manual.component';
import { ManualDiagnosisComponent } from './manual-diagnosis/manual-diagnosis.component';

const routes: Routes = [
  {
    path: 'graphs',
    component: VisualizationComponent,
  },
  {
    path: 'upload-manual',
    component: UploadManualComponent,
  },
  {
    path: 'diagnosis_view',
    component: ManualDiagnosisComponent,
  },
  {
    path: '',
    pathMatch: 'full',
    redirectTo: 'graphs',
  },
];

@NgModule({
  declarations: [
    VisualizationComponent,
    UploadManualComponent,
    ManualDiagnosisComponent,
  ],
  imports: [
    CommonModule,
    WorkSpaceModule,
    RouterModule.forChild(routes),
    FormsModule,
  ],
})
export class AiModule {}
