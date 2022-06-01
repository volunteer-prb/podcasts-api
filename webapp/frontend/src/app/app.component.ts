import {Component, OnInit} from '@angular/core';
import {Toast} from "./classes/core/toast";
import {LoggerService} from "./services/logger.service";
import {ActivatedRoute, NavigationEnd, Router} from "@angular/router";
import {filter} from "rxjs";

class NavItem {
  constructor(public title: string = '', public url: string[] = [], public icon: string = '') {
  }
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit{
  appTitle = 'Podcasts service';

  private _showNav: boolean = false
  private _showNavDelayed: boolean = false
  private _showNavDelayedTimer: number|undefined = undefined
  set showNav(value: boolean) {
    this._showNav = value;
    if (value) {
      this._showNavDelayed = true;
    } else {
      clearTimeout(this._showNavDelayedTimer)
      this._showNavDelayedTimer = setTimeout(() => {this._showNavDelayed = false}, 500);
    }
  }
  get showNav(): boolean {
    return this._showNav
  }
  get showNavDelayed(): boolean {
    return this._showNavDelayed
  }

  navItems = [
    new NavItem('Source channels', ['channels'], 'bi-broadcast'),
  ]
  currentNav: string[] | undefined = []

  toasts: Toast[] = [];

  constructor(private logger: LoggerService,
              private router: Router,
              private route: ActivatedRoute,
              ) {
  }

  ngOnInit(): void {
    this.logger.event.subscribe(toast => {
      this.toasts.push(toast);
      if (toast.timeout > 0) {
        setTimeout(() => {
          this.deleteToast(toast.id);
        }, toast.timeout);
      }
    });

    this.router.events.pipe(filter(event => event instanceof NavigationEnd)).subscribe(event => {
      this.currentNav = this.route.snapshot.firstChild?.url.map(value => value.path)
      this.showNav = false
    })
  }

  deleteToast(toastId: number): void {
    this.toasts = this.toasts.filter(t => t.id !== toastId);
  }

  isActive(url: string[]) {
    if (this.currentNav === undefined) return false
    if (this.currentNav.length !== url.length) return false
    return url
      .map((value, index) => this.currentNav !== undefined && value === this.currentNav[index])
      .reduce((a, b) => a && b)
  }
}
