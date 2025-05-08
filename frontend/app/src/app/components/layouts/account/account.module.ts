import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from './header-account/header.component';
import { SidenavComponent } from './sidenav-account/sidenav.component';
import { LucideAngularModule, Settings, User } from 'lucide-angular';
import { RouterModule } from '@angular/router';



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
export class AccountModule { }
