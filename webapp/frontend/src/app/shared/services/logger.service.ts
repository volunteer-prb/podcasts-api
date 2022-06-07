import { EventEmitter, Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';
import { Toast } from '../core/toast';

@Injectable({
  providedIn: 'root',
})
export class LoggerService {
  private eventId = 0;
  event: EventEmitter<Toast> = new EventEmitter<Toast>();

  constructor() {}

  info(...args: any[]) {
    if (!environment.production) {
      console.warn('INFO', ...args);
    }
  }

  warn(...args: any[]) {
    if (!environment.production) {
      console.warn('WARN', ...args);
      this.event.emit(this.getToast(...args));
    }
  }

  error(...args: any[]) {
    if (!environment.production) {
      console.error('ERROR', ...args);
      this.event.emit(this.getToast(...args));
    }
  }

  errorMessage(
    header: string,
    body: string | undefined,
    timeout: number = 60000
  ): void {
    if (body === undefined) {
      body = 'Internal service error';
    }
    this.eventId++;
    const toast = new Toast();
    toast.header = header;
    toast.body = body;
    toast.timeout = timeout;
    toast.id = this.eventId;
    toast.error = true;
    this.event.emit(toast);
  }

  getToast(...args: any[]): Toast {
    const toast = new Toast();
    toast.header = args[0];
    toast.body = args
      .map((v) => (typeof v == 'string' ? v : JSON.stringify(v)))
      .join(' ');
    toast.id = this.eventId;
    toast.error = true;
    this.eventId++;
    return toast;
  }
}
