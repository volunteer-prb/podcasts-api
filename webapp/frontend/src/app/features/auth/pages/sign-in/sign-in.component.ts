import { HttpErrorResponse } from '@angular/common/http';
import { AuthService } from '@features/auth/services/auth.service';
import { AppRoutes } from '@core/values/app-routes.enum';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { User } from '@core/api/models/user.model';
import { validateEmail } from '@features/auth/validators/validate-email';

interface FormModel {
  email: string;
  password: string;
}

@Component({
  selector: 'sign-in',
  templateUrl: './sign-in.component.html',
  styleUrls: ['./sign-in.component.scss'],
})
export class SignInComponent implements OnInit, OnDestroy {
  private readonly subscriptions = new Subscription();

  private user: User;

  form: FormGroup;

  get isValidForm(): boolean {
    return this.form.controls['email'].valid && this.form.controls['password'].valid;
  }

  get isInvalidEmail(): boolean {
    return this.form.controls['email'].invalid && this.form.controls['email'].dirty;
  }

  get isInvalidPassword(): boolean {
    return this.form.controls['password'].invalid && this.form.controls['password'].dirty;
  }

  constructor(private readonly router: Router, private readonly authService: AuthService) {}

  ngOnInit() {
    this.initFormGroup();

    this.subscriptions.add(
      this.form.valueChanges.subscribe((user: FormModel) => {
        this.user = user;
      }),
    );
  }

  ngOnDestroy() {
    this.subscriptions.unsubscribe();
  }

  private initFormGroup() {
    this.form = new FormGroup({
      email: new FormControl('', [Validators.required, validateEmail]),
      password: new FormControl('', [Validators.required, Validators.minLength(6)]),
    });
  }

  private handelSuccessAuth = (e: any) => {
    console.log(e);
    this.router.navigate([AppRoutes.CHANNELS]);
  };

  private handleError = (error: HttpErrorResponse) => {
    // TODO: show toast with error
    console.warn(error);
  };

  navigateToSignUp() {
    this.router.navigate([AppRoutes.AUTH, AppRoutes.SIGN_UP], { replaceUrl: true });
  }

  onClickLoginButton() {
    this.subscriptions.add(
      this.authService.login(this.user).subscribe(this.handelSuccessAuth, this.handleError),
    );
  }
}
