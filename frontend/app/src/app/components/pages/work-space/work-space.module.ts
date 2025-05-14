import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HomeComponent } from './home/home.component';
import { ResultsComponent } from './results/results.component';
import { PatientsComponent } from './patients/patients.component';
import { SettingsComponent } from './settings/settings.component';
import { HelpComponent } from './help/help.component';
import { Routes } from '@angular/router';
import { RouterModule } from '@angular/router';
import { LayoutsModule } from '../../layouts/layouts.module';

const routes: Routes = [
  {
    path: 'home',
    component: HomeComponent,
  },
  {
    path: 'upload',
    loadChildren: () =>
      import('./upload/upload.module').then(m => m.UploadModule)
  },
  {
    path: 'results',
    component: ResultsComponent,
  },
  {
    path: 'patients',
    component: PatientsComponent,
  },
  {
    path: 'settings',
    component: SettingsComponent,
  },
  {
    path: 'help',
    component: HelpComponent,
  },
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full',
  },
  {
    path: '**',
    redirectTo: 'home',
  },
];

@NgModule({
  declarations: [
    HomeComponent,
    ResultsComponent,
    PatientsComponent,
    SettingsComponent,
    HelpComponent,
  ],
  imports: [CommonModule, RouterModule.forChild(routes), LayoutsModule],
  exports: [RouterModule],
})
export class WorkSpaceModule {}
