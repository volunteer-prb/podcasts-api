import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AppRoutes } from '@core/values/app-routes.enum';
import { BehaviorSubject, map, Observable } from 'rxjs';

enum SignUpStates {
  EMAIL = 'email',
  PASSWORD = 'password',
}

enum Subtitles {
  EMAIL = 'Введите свой email',
  PASSWORD = 'Придумайте пароль',
}

@Component({
  selector: 'sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.scss'],
})
export class SignUpComponent {
  readonly signUpStates = SignUpStates;

  readonly currentSignUpState$ = new BehaviorSubject<SignUpStates>(SignUpStates.EMAIL);

  readonly subtitle$: Observable<string> = this.currentSignUpState$.pipe(
    map((state) => (state === SignUpStates.EMAIL ? Subtitles.EMAIL : Subtitles.PASSWORD)),
  );

  constructor(private readonly router: Router) {}

  navigateToSignIn() {
    this.router.navigate([AppRoutes.AUTH, AppRoutes.SIGN_IN], { replaceUrl: true });
  }
}
