import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ImageComponent } from './image/image.component';
import { VisualizationComponent } from './visualization/visualization.component';
import { RouterModule, Routes } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { WorkSpaceModule } from '../../../layouts/work-space/work-space.module';
import { LucideAngularModule } from 'lucide-angular';


const routes: Routes = [
  {
    path: 'image',
    component: ImageComponent
  },
  {
    path: 'visualization',
    component: VisualizationComponent
  },
  {
    path: '',
    redirectTo: 'image',
    pathMatch: 'full'
  },
];

@NgModule({
  declarations: [
    ImageComponent,
    VisualizationComponent,
  ],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    FormsModule,
    WorkSpaceModule,
    LucideAngularModule
  ],
  exports: [
      RouterModule
  ]

})
export class UploadModule { }
