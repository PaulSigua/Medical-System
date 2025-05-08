import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AccountComponent } from './account/account.component';
import { RouterModule, Routes } from '@angular/router';
import { SettingsComponent } from './settings/settings.component';
import { InformationComponent } from './account/information/information.component';
import { PasswordComponent } from './account/password/password.component';
import { Lock, LucideAngularModule, User } from 'lucide-angular';
import { AccountModule } from '../../layouts/account/account.module';
import { GeneralComponent } from './settings/general/general.component';
import { ViewingComponent } from './settings/viewing/viewing.component';

const routes: Routes = [
  {
    path: 'account',
    component: AccountComponent,
    children: [
      { path: '', redirectTo: 'info', pathMatch: 'full' },
      { path: 'info', component: InformationComponent },
      { path: 'change-password', component: PasswordComponent }
    ]
  },
  {
    path: 'settings',
    component: SettingsComponent,
    children: [
      {
        path: '',
        redirectTo: 'general',
        pathMatch: 'full'
      },
      {
        path: 'general',
        component: GeneralComponent,
      },
      {
        path: 'viewing',
        component: ViewingComponent,
      }
    ]
  },
  {
    path: '',
    redirectTo: 'account',
    pathMatch: 'full'
  },
]

@NgModule({
  declarations: [
    AccountComponent,
    SettingsComponent,
    InformationComponent,
    PasswordComponent,
    GeneralComponent,
    ViewingComponent
  ],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    AccountModule,
    LucideAngularModule.pick({
      User,
      Lock,
    }),
  ],
  exports: [
    RouterModule
  ],
})
export class UserModule { }
