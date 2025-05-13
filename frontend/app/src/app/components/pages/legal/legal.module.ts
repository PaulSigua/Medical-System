import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TermsComponent } from './terms/terms.component';
import { RouterModule } from '@angular/router';
import { LucideAngularModule} from 'lucide-angular';
import { PrivacyComponent } from './privacy/privacy.component';



@NgModule({
  declarations: [
    TermsComponent,
    PrivacyComponent
  ],
  imports: [
    CommonModule,
    RouterModule.forChild([
      {
        path: 'terms',
        component: TermsComponent
      },
      {
        path: 'privacy',
        component: PrivacyComponent
      }
    ]),
    LucideAngularModule
  ]
})
export class LegalModule { }
