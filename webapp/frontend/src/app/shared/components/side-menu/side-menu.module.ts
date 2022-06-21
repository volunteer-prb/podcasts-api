import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';
import { SideMenuComponent } from './side-menu.component';

@NgModule({
  imports: [RouterModule, CommonModule],
  declarations: [SideMenuComponent],
  exports: [SideMenuComponent],
})
export class SideMenuModule {}
