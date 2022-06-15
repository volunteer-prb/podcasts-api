import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { AuthApi } from './api/services/auth.api';

@NgModule({
  imports: [HttpClientModule],
  providers: [AuthApi],
})
export class CoreModule {}
