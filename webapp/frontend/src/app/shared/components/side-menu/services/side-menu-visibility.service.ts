import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable()
export class SideMenuVisibilityService {
  private readonly isVisible = new BehaviorSubject(false);

  get isVisible$(): Observable<boolean> {
    return this.isVisible.asObservable();
  }

  setVisibility(isVisible: boolean) {
    this.isVisible.next(isVisible);
  }
}
