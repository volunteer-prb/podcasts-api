import { AppRoutes } from '@core/values/app-routes.enum';
import { AuthService } from '@features/auth/services/auth.service';
import { RouteDataParams } from '@core/types/route-data-params.type';
import { MenuRoutes } from './values/menu-routes.const';
import { Component, OnInit, OnDestroy, ChangeDetectionStrategy } from '@angular/core';
import { filter, map, Observable, Subscription, switchMap } from 'rxjs';
import { ActivatedRoute, NavigationEnd, Router } from '@angular/router';
import { SideMenuVisibilityService } from './services/side-menu-visibility.service';

@Component({
  selector: 'side-menu',
  templateUrl: './side-menu.component.html',
  styleUrls: ['./side-menu.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SideMenuComponent implements OnInit, OnDestroy {
  private readonly subscriptions = new Subscription();

  readonly menuRoutes = MenuRoutes;

  get isShow$(): Observable<boolean> {
    return this.sideMenuVisibilityService.isVisible$;
  }

  constructor(
    private router: Router,
    private activatedRoute: ActivatedRoute,
    private authService: AuthService,
    private sideMenuVisibilityService: SideMenuVisibilityService,
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
          this.sideMenuVisibilityService.setVisibility(params.hasMenu ?? true);
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
