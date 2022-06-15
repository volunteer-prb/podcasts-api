import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AppRoutes } from '@core/values/app-routes.enum';
import { BehaviorSubject, map, Observable, Subscription } from 'rxjs';

enum SignUpStates {
  EMAIL = 'email',
  PASSWORD = 'password',
}

enum Subtitles {
  EMAIL = 'Введите свой email',
  PASSWORD = 'Придумайте пароль',
}

interface FormModel {
  email: string;
  password: string;
  confirmPassword: string;
}

@Component({
  selector: 'sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.scss'],
})
export class SignUpComponent implements OnInit, OnDestroy {
  private readonly subscriptions = new Subscription();

  readonly signUpStates = SignUpStates;

  readonly currentSignUpState$ = new BehaviorSubject<SignUpStates>(SignUpStates.EMAIL);

  readonly subtitle$: Observable<string> = this.currentSignUpState$.pipe(
    map((state) => (state === SignUpStates.EMAIL ? Subtitles.EMAIL : Subtitles.PASSWORD)),
  );

  private get isValidPassword(): boolean {
    return (
      this.form.controls['password'].valid &&
      this.form.controls['confirmPassword'].valid &&
      this.form.controls['password'].value === this.form.controls['confirmPassword'].value
    );
  }

  get isDisabledButton(): boolean {
    return this.currentSignUpState$.value === SignUpStates.EMAIL
      ? this.form.controls['email'].invalid
      : !this.isValidPassword;
  }

  form: FormGroup;

  constructor(private readonly router: Router) {}

  ngOnInit() {
    this.initFormGroup();

    this.subscriptions.add(
      this.form.valueChanges.subscribe((r: FormModel) => {
        console.log(r);
      }),
    );

    this.subscriptions.add();
  }

  ngOnDestroy() {
    this.subscriptions.unsubscribe();
  }

  private initFormGroup() {
    this.form = new FormGroup({
      email: new FormControl('', [Validators.required, Validators.email]),
      password: new FormControl('', [Validators.required, Validators.minLength(6)]),
      confirmPassword: new FormControl('', [Validators.required, Validators.minLength(6)]),
    });
  }

  navigateToSignIn() {
    this.router.navigate([AppRoutes.AUTH, AppRoutes.SIGN_IN], { replaceUrl: true });
  }

  onClickRegisterButton() {
    if (this.currentSignUpState$.value === SignUpStates.EMAIL)
      this.currentSignUpState$.next(SignUpStates.PASSWORD);
  }
}
