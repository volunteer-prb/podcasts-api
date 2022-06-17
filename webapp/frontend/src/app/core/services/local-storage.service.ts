import { Injectable } from '@angular/core';
import { BaseStorage } from './base-storage';

@Injectable({
  providedIn: 'root',
})
export class LocalStorageService extends BaseStorage {
  constructor() {
    super(localStorage);
  }
}
