import { AppRoutes } from '@core/values/app-routes.enum';
import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'sign-in',
  templateUrl: './sign-in.component.html',
  styleUrls: ['./sign-in.component.scss'],
})
export class SignInComponent {
  constructor(private readonly router: Router) {}

  navigateToSignUp() {
    this.router.navigate([AppRoutes.AUTH, AppRoutes.SIGN_UP], { replaceUrl: true });
  }
}
