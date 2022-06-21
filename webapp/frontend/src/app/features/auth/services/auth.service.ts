import { StorageKeys } from '@core/values/storage-keys.enum';
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
    private readonly sessionStorageService: SessionStorageService,
  ) {
    const authState = sessionStorageService.getItem<boolean>(StorageKeys.AUTH_STATE);
    this.isAuthorized$.next(!!authState);
  }

  private handleSuccessAuth = () => {
    this.sessionStorageService.setItem(StorageKeys.AUTH_STATE, true);

    this.isAuthorized$.next(true);
  };

  private handleLogout = () => {
    this.sessionStorageService.setItem(StorageKeys.AUTH_STATE, false);

    this.isAuthorized$.next(false);
  };

  login(user: User): Observable<AuthResponse> {
    return this.authApi.login(user).pipe(tap(this.handleSuccessAuth));
  }

  register(user: User): Observable<AuthResponse> {
    return this.authApi.register(user).pipe(tap(this.handleSuccessAuth));
  }

  logout() {
    this.sessionStorageService.clear();
  }
}
