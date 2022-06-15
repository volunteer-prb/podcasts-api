import { AppRoutes } from '@core/values/app-routes.enum';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { FormControl, FormGroup, Validators } from '@angular/forms';

// interface FormModel {
//   email: string;
//   password: string;
// }

@Component({
  selector: 'sign-in',
  templateUrl: './sign-in.component.html',
  styleUrls: ['./sign-in.component.scss'],
})
export class SignInComponent implements OnInit, OnDestroy {
  private readonly subscriptions = new Subscription();

  form: FormGroup;

  get isValidForm(): boolean {
    return this.form.controls['email'].valid && this.form.controls['password'].valid;
  }

  constructor(private readonly router: Router) {}

  ngOnInit() {
    this.initFormGroup();
  }

  ngOnDestroy() {
    this.subscriptions.unsubscribe();
  }

  private initFormGroup() {
    this.form = new FormGroup({
      email: new FormControl('', [Validators.required, Validators.email]),
      password: new FormControl('', [Validators.required, Validators.minLength(6)]),
    });
  }

  navigateToSignUp() {
    this.router.navigate([AppRoutes.AUTH, AppRoutes.SIGN_UP], { replaceUrl: true });
  }

  onClickLoginButton() {
    console.log('onClickLoginButton');
  }
}
