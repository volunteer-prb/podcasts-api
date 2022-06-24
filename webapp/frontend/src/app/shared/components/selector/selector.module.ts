import { CommonModule } from '@angular/common';
import { SelectorComponent } from './selector.component';
import { NgModule } from '@angular/core';
import { MatSelectModule } from '@angular/material/select';

@NgModule({
  imports: [MatSelectModule, CommonModule],
  exports: [SelectorComponent],
  declarations: [SelectorComponent],
})
export class SelectorModule {}
