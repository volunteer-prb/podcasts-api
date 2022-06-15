import { Injectable } from '@angular/core';
import { BaseStorage } from './base-storage';

@Injectable({
  providedIn: 'root',
})
export class SessionStorageService extends BaseStorage {
  constructor() {
    super(sessionStorage);
  }
}
