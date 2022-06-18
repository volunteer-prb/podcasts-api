import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { User } from '@core/api/models/user.model';
import { ApiContrillers } from '@core/api/values/api-controllers.enum';
import { Observable } from 'rxjs';
import { AuthResponse } from '@core/api/models/auth-response.model';
import { getMockSignInResponse, getMockSignUpResponse } from '@core/api/__moks__/success-auth';

@Injectable()
export class AuthApi {
  constructor(private readonly http: HttpClient) {}

  register(user: User): Observable<AuthResponse<{}>> {
    return getMockSignUpResponse(user);

    // TODO: Change api endpoints
    return this.http.post<AuthResponse<{}>>(
      `${ApiContrillers.AUTH}/${ApiContrillers.REGISTER}`,
      user,
    );
  }

  login(user: User): Observable<AuthResponse<{}>> {
    return getMockSignInResponse(user);

    // TODO: Change api endpoints
    return this.http.post<AuthResponse<{}>>(`${ApiContrillers.AUTH}/${ApiContrillers.LOGIN}`, user);
  }
}
