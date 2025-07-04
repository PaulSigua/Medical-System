import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ImageComponent } from './image/image.component';
import { VisualizationComponent } from './visualization/visualization.component';
import { RouterModule, Routes } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { WorkSpaceModule } from '../../../layouts/work-space/work-space.module';
import { LucideAngularModule } from 'lucide-angular';
import { GraphsModule } from "../../../layouts/graphs/graphs.module";
import { SegmentationComponent } from './segmentation/segmentation.component';


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
    path: 'segmentation',
    component: SegmentationComponent
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
    SegmentationComponent,
  ],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    FormsModule,
    WorkSpaceModule,
    LucideAngularModule,
    GraphsModule
],
  exports: [
      RouterModule
  ]

})
export class UploadModule { }
