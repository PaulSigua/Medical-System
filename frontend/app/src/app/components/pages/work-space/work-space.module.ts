import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HomeComponent } from './home/home.component';
import { PredictionComponent } from './prediction/prediction.component';
import { ResultsComponent } from './results/results.component';
import { PatientsComponent } from './patients/patients.component';
import { SettingsComponent } from './settings/settings.component';
import { HelpComponent } from './help/help.component';
import { Routes } from '@angular/router';
import { RouterModule } from '@angular/router';
import { WorkSpaceModule as LayoutWorkSpaceModule } from "../../layouts/work-space/work-space.module";

const routes: Routes = [
  {
    path: 'home',
    component: HomeComponent
  },
  {
    path: 'prediction',
    component: PredictionComponent
  },
  {
    path: 'results',
    component: ResultsComponent
  },
  {
    path: 'patients',
    component: PatientsComponent
  },
  {
    path: 'settings',
    component: SettingsComponent
  },
  {
    path: 'help',
    component: HelpComponent
  },
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full'
  },
  {
    path: '**',
    redirectTo: 'home'
  }
];

@NgModule({
  declarations: [
    HomeComponent,
    PredictionComponent,
    ResultsComponent,
    PatientsComponent,
    SettingsComponent,
    HelpComponent
  ],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    LayoutWorkSpaceModule,
],
  exports: [
    RouterModule
  ]
})
export class WorkSpaceModule { }
