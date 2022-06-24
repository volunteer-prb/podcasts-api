import { MatIconModule } from '@angular/material/icon';
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { PlayerComponent } from './player.component';
import { MinuteSecondsPipe } from './pipes/minute-seconds.pipe';

@NgModule({
  imports: [CommonModule, MatIconModule],
  exports: [PlayerComponent],
  declarations: [PlayerComponent, MinuteSecondsPipe],
})
export class PlayerModule {}
