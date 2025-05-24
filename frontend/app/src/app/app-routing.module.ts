import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from './guards/auth/auth.guard';
import { PublicGuard } from './guards/public/public.guard';

const routes: Routes = [
  {
    path: 'auth',
    loadChildren: () =>
      import('./components/pages/auth/auth.module').then((m) => m.AuthModule),
    canActivate: [PublicGuard],
  },
  {
    path: 'work-space',
    loadChildren: () =>
      import('./components/pages/work-space/work-space.module').then(
        (m) => m.WorkSpaceModule
      ),
    canActivate: [AuthGuard],
  },
  {
    path: 'user',
    loadChildren: () =>
      import('./components/pages/user/user.module').then((m) => m.UserModule),
    canActivate: [AuthGuard],
  },
  {
    path: 'legal',
    loadChildren: () =>
      import('./components/pages/legal/legal.module').then(
        (m) => m.LegalModule
      ),
    canActivate: [PublicGuard],
  },
  {
    path: 'upload',
    loadChildren: () =>
      import('./components/pages/work-space/upload/upload.module').then(
        (m) => m.UploadModule
      ),
    canActivate: [AuthGuard],
  },
  {
    path: 'ia',
    loadChildren: () => 
      import('./components/pages/work-space/ia/ia.module').then(
        (m) => m.IaModule
      ),
      canActivate: [AuthGuard],
  },
  {
    path: '',
    redirectTo: 'auth',
    pathMatch: 'full',
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
