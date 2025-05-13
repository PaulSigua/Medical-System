import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {
    path: 'auth',
    loadChildren: () => import('./components/pages/auth/auth.module').then(m => m.AuthModule)
  },
  {
    path: 'work-space',
    loadChildren: () => import('./components/pages/work-space/work-space.module').then(m => m.WorkSpaceModule)
  },
  {
    path: 'user',
    loadChildren: () => import('./components/pages/user/user.module').then(m => m.UserModule)
  },
  {
    path: 'legal',
    loadChildren: () => import('./components/pages/legal/legal.module').then(m => m.LegalModule)
  },
  {
    path: '',
    redirectTo: 'auth',
    pathMatch: 'full'
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
