import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HistogramComponent } from './histogram/histogram.component';



@NgModule({
  declarations: [
    HistogramComponent
  ],
  imports: [
    CommonModule
  ],
  exports: [
    HistogramComponent
  ],
  providers: []
})
export class ChartsModule { }
