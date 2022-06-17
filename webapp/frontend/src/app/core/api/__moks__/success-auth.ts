import { HttpErrorResponse } from '@angular/common/http';
import { of, throwError } from 'rxjs';
import { AuthResponse } from '../models/auth-response.model';
import { User } from '../models/user.model';

export const SuccessAuth: AuthResponse = {
  message: 'success',
};

export const mockUser: User = {
  email: 'qwe@qwe.qwe',
  password: 'qweqwe',
};

export const getMockSignInResponse = ({ email, password }: User) => {
  return email === 'qwe@qwe.qwe' && password === 'qweqwe'
    ? of(SuccessAuth)
    : throwError(() => new HttpErrorResponse({ status: 401, statusText: 'sign in' }));
};

export const getMockSignUpResponse = ({ email }: User) => {
  return email !== 'qwe@qwe.qwe'
    ? of(SuccessAuth)
    : throwError(() => new HttpErrorResponse({ status: 401, statusText: 'sign up' }));
};
