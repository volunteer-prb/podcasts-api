import { HttpErrorResponse } from '@angular/common/http';
import { of, throwError } from 'rxjs';
import { AuthResponse } from '../models/auth-response.model';
import { ErrorResponse } from '../models/error-response.model';
import { User } from '../models/user.model';

const successAuth: AuthResponse<{}> = {
  status: 'success',
  data: {},
};

const errorResponse: ErrorResponse = {
  status: 'success',
  message: 'Auth error message',
};

const mockUser: User = {
  email: 'qwe@qwe.qwe',
  password: 'qweqwe',
};

export const getMockSignInResponse = ({ email, password }: User) => {
  return email === mockUser.email && password === mockUser.password
    ? of(successAuth)
    : throwError(
        () => new HttpErrorResponse({ status: 401, statusText: 'sign in', error: errorResponse }),
      );
};

export const getMockSignUpResponse = ({ email }: User) => {
  return email !== mockUser.email
    ? of(successAuth)
    : throwError(
        () => new HttpErrorResponse({ status: 401, statusText: 'sign up', error: errorResponse }),
      );
};
