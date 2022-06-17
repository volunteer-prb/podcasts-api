import { HttpHeaderInterceptor } from './interceptors/http-header.interceptor';
import { ProxyInterceptor } from './interceptors/proxy.interceptor';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { AuthApi } from './api/services/auth.api';

@NgModule({
  imports: [HttpClientModule],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: ProxyInterceptor,
      multi: true,
    },
    {
      provide: HTTP_INTERCEPTORS,
      useClass: HttpHeaderInterceptor,
      multi: true,
    },
    AuthApi,
  ],
})
export class CoreModule {}
