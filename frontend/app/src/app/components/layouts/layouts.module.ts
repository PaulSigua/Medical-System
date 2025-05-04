import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NavComponent } from './nav/nav.component';
import { SidenavComponent } from './sidenav/sidenav.component';
import { FooterComponent } from './footer/footer.component';



@NgModule({
  declarations: [
    NavComponent,
    SidenavComponent,
    FooterComponent
  ],
  imports: [
    CommonModule
  ]
})
export class LayoutsModule { }
