import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoginComponent } from './login/login.component';
import { SigninComponent } from './signin/signin.component';
import { Routes } from '@angular/router';
import { RouterModule } from '@angular/router';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { AuthLayoutModule } from '../../layouts/auth/auth-layout.module';
import { JwtModule } from '@auth0/angular-jwt';
import { environment } from '../../../../environments/environment.development';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
import { TokenInterceptor } from '../../../interceptors/auth/auth.interceptor';
import { ResetPasswordComponent } from './reset-password/reset-password.component';
import { RequestResetComponent } from './request-reset/request-reset.component';

const routes: Routes = [
  {
    path: 'login',
    component: LoginComponent,
  },
  {
    path: 'signin',
    component: SigninComponent,
  },
  {
    path: 'request-reset',
    component: RequestResetComponent,
  },
  {
    path: 'reset-password',
    component: ResetPasswordComponent,
  },
  {
    path: '',
    redirectTo: 'login',
    pathMatch: 'full',
  },
];

export function tokenGetter() {
  return localStorage.getItem('access_token');
}

let HOST_API: string = environment.HOST_API;
let API_URL: string = environment.API_URL;

@NgModule({
  declarations: [
    LoginComponent,
    SigninComponent,
    ResetPasswordComponent,
    RequestResetComponent,
  ],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    ReactiveFormsModule,
    AuthLayoutModule,
    JwtModule.forRoot({
      config: {
        tokenGetter: tokenGetter,
        allowedDomains: [HOST_API],
        disallowedRoutes: [`${API_URL}/auth/login`, `${API_URL}/auth/register`],
      },
    }),
    HttpClientModule,
    FormsModule,
  ],
  exports: [RouterModule],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: TokenInterceptor,
      multi: true,
    },
  ],
})
export class AuthModule {}
