import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';
import { SideMenuComponent } from './side-menu.component';
import { SideMenuVisibilityService } from './services/side-menu-visibility.service';

@NgModule({
  imports: [RouterModule, CommonModule],
  declarations: [SideMenuComponent],
  providers: [SideMenuVisibilityService],
  exports: [SideMenuComponent],
})
export class SideMenuModule {}
