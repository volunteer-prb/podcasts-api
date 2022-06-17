import { AppRoutes } from '@core/values/app-routes.enum';
import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { AuthService } from '@features/auth/services/auth.service';

@Injectable({
  providedIn: 'root',
})
export class AuthGuard implements CanActivate {
  constructor(private authService: AuthService, private router: Router) {}

  canActivate(): boolean {
    if (this.authService.isAuthorized) return true;

    this.router.navigate([AppRoutes.AUTH], { replaceUrl: true });

    return false;
  }
}
