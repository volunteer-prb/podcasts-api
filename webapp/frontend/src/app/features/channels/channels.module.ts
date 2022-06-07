import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChannelsComponent } from './components/channels.component';
import { SharedModule } from '@shared/shared.module';
import { ChannelsRoutingModule } from './channels-routing.module';

@NgModule({
  declarations: [ChannelsComponent],
  imports: [CommonModule, SharedModule, ChannelsRoutingModule],
})
export class ChannelsModule {}
