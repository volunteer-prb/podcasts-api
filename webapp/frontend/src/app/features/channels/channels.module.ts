import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChannelsComponent } from './channels.component';
import { SharedModule } from '@shared/shared.module';
import { ChannelsRoutingModule } from './channels-routing.module';
import { HeadingModule } from '@shared/components/heading/heading.module';

@NgModule({
  declarations: [ChannelsComponent],
  imports: [CommonModule, SharedModule, ChannelsRoutingModule, HeadingModule],
})
export class ChannelsModule {}
