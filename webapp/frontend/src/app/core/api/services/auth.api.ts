import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { User } from '@core/api/models/user.model';
import { ApiContrillers } from '@core/api/values/api-controllers.enum';
import { Observable, of } from 'rxjs';
import { AuthResponse } from '@core/api/models/auth-response.model';
import { SuccessAuth } from '@core/api/__moks__/success-auth';

@Injectable()
export class AuthApi {
  constructor(private readonly http: HttpClient) {}

  register(user: User): Observable<AuthResponse> {
    return of(SuccessAuth);

    // TODO: Change api endpoints
    return this.http.post<AuthResponse>(`${ApiContrillers.AUTH}/${ApiContrillers.REGISTER}`, user);
  }

  login(user: User): Observable<AuthResponse> {
    return of(SuccessAuth);

    // TODO: Change api endpoints
    return this.http.post<AuthResponse>(`${ApiContrillers.AUTH}/${ApiContrillers.LOGIN}`, user);
  }

  logout() {
    // TODO: Create request
  }
}
