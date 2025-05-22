import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { GraphViewerComponent } from './graph-viewer/graph-viewer.component';



@NgModule({
  declarations: [
    GraphViewerComponent
  ],
  imports: [
    CommonModule
  ],
  exports: [
    GraphViewerComponent
  ]
})
export class GraphsModule { }
