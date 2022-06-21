import { AppRoutes } from '@core/values/app-routes.enum';
import { AuthService } from '@features/auth/services/auth.service';
import { RouteDataParams } from '@core/types/route-data-params.type';
import { MenuRoutes } from './values/menu-routes.const';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { filter, map, Observable, Subscription, switchMap } from 'rxjs';
import { ActivatedRoute, NavigationEnd, Router } from '@angular/router';

@Component({
  selector: 'side-menu',
  templateUrl: './side-menu.component.html',
  styleUrls: ['./side-menu.component.scss'],
})
export class SideMenuComponent implements OnInit, OnDestroy {
  private readonly subscriptions = new Subscription();

  readonly menuRoutes = MenuRoutes;

  isHidden = true;

  constructor(
    private router: Router,
    private activatedRoute: ActivatedRoute,
    private authService: AuthService,
  ) {}

  ngOnInit() {
    this.subscriptions.add(
      this.router.events
        .pipe(
          filter((event) => event instanceof NavigationEnd),
          map(() => this.activatedRoute.firstChild),
          switchMap((route) => route?.data as Observable<RouteDataParams>),
        )
        .subscribe((params) => {
          this.isHidden = !(params.hasMenu ?? true);
        }),
    );
  }

  ngOnDestroy() {
    this.subscriptions.unsubscribe();
  }

  logout() {
    this.authService.logout();

    this.router.navigate([AppRoutes.AUTH]);
  }
}
