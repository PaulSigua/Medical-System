import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FooterAuthComponent } from './footer-auth/footer-auth.component';
import { RouterModule } from '@angular/router';



@NgModule({
  declarations: [
    FooterAuthComponent
  ],
  imports: [
      CommonModule,
      RouterModule
  ],
  exports: [
    FooterAuthComponent
  ]
  
})
export class AuthLayoutModule { }
