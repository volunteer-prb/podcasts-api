import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { HeadingComponent } from './components/heading/heading.component';
import { MatMenuModule } from '@angular/material/menu';
import { MatIconModule } from '@angular/material/icon';
import { AccountPanelComponent } from './components/account-panel/account-panel.component';

@NgModule({
  imports: [CommonModule, MatMenuModule, MatIconModule],
  exports: [HeadingComponent],
  declarations: [HeadingComponent, AccountPanelComponent],
})
export class HeadingModule {}
