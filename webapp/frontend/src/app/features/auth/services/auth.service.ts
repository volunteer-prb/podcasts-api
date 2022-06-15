import { AuthApi } from '@core/api/services/auth.api';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { User } from '@core/api/models/user.model';
import { AuthResponse } from '@core/api/models/auth-response.model';
import { SessionStorageService } from '@core/services/session-storage.service';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private readonly isAuthorized$ = new BehaviorSubject<boolean>(false);

  get isAuthorized(): boolean {
    return this.isAuthorized$.value;
  }

  constructor(
    private readonly authApi: AuthApi,
    private sessionStorageService: SessionStorageService,
  ) {}

  private setSuccessAuth = () => {
    this.isAuthorized$.next(true);
  };

  login(user: User): Observable<AuthResponse> {
    return this.authApi.login(user).pipe(tap(this.setSuccessAuth));
  }

  register(user: User): Observable<AuthResponse> {
    return this.authApi.register(user).pipe(tap(this.setSuccessAuth));
  }
}
