import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from './header-ws/header.component';
import { SidenavComponent } from './sidenav-ws/sidenav.component';
import { RouterModule } from '@angular/router';
import { LucideAngularModule } from 'lucide-angular';



@NgModule({
  declarations: [
    HeaderComponent,
    SidenavComponent
  ],
  imports: [
    CommonModule,
    RouterModule,
    LucideAngularModule
  ],
  exports: [
    HeaderComponent,
    SidenavComponent
  ]
})
export class WorkSpaceModule { }
