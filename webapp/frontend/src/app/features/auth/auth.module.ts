import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { AuthRoutingModule } from './auth-routing.module';
import { AuthComponent } from './auth.component';
import { SignInComponent } from './pages/sign-in/sign-in.component';
import { SignUpComponent } from './pages/sign-up/sign-up.component';
import { LogoComponent } from './components/logo/logo.component';
import { InputFieldComponent } from './components/input-field/input-field.component';
import { ButtonModule } from '@shared/components/button/button.module';
import { CheckboxModule } from '@shared/components/checkbox/checkbox.module';
import { GoogleButtonComponent } from './components/google-button/google-button.component';
import { ReactiveFormsModule } from '@angular/forms';

@NgModule({
  imports: [AuthRoutingModule, CommonModule, ReactiveFormsModule, ButtonModule, CheckboxModule],
  declarations: [
    AuthComponent,
    SignInComponent,
    SignUpComponent,
    LogoComponent,
    InputFieldComponent,
    GoogleButtonComponent,
  ],
})
export class AuthModule {}
