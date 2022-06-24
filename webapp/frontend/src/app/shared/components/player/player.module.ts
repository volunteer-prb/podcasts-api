import { MatIconModule } from '@angular/material/icon';
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { PlayerComponent } from './player.component';

@NgModule({
  imports: [CommonModule, MatIconModule],
  exports: [PlayerComponent],
  declarations: [PlayerComponent],
})
export class PlayerModule {}
