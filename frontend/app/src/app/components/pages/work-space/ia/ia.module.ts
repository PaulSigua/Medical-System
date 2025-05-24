import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { VisualizationComponent } from './visualization/visualization.component';
import { WorkSpaceModule } from '../../../layouts/work-space/work-space.module';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {
    path: 'graphs',
    component: VisualizationComponent
  },
  {
    path: '',
    pathMatch: 'full',
    redirectTo: 'graphs'
  }
]

@NgModule({
  declarations: [
    VisualizationComponent
  ],
  imports: [
    CommonModule,
    WorkSpaceModule,
    RouterModule.forChild(routes)
  ]
})
export class IaModule { }
