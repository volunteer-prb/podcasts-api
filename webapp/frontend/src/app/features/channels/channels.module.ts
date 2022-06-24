import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChannelsComponent } from './channels.component';
import { SharedModule } from '@shared/shared.module';
import { ChannelsRoutingModule } from './channels-routing.module';
import { HeadingModule } from '@shared/components/heading/heading.module';
import { PodcastCardComponent } from './components/podcast-card/podcast-card.component';
import { MatIconModule } from '@angular/material/icon';
import { MatMenuModule } from '@angular/material/menu';
import { ChannelsFilterComponent } from './components/channels-filter/channels-filter.component';
import { ButtonModule } from '@shared/components/button/button.module';
import { SwiperModule } from 'swiper/angular';
import SwiperCore, { Navigation } from 'swiper';
import { SliderComponent } from './components/slider/slider.component';
import { CheckboxModule } from '@shared/components/checkbox/checkbox.module';
import { SelectorModule } from '@shared/components/selector/selector.module';
import { PlayerModule } from '@shared/components/player/player.module';

SwiperCore.use([Navigation]);

@NgModule({
  declarations: [ChannelsComponent, PodcastCardComponent, ChannelsFilterComponent, SliderComponent],
  imports: [
    CommonModule,
    SharedModule,
    ChannelsRoutingModule,
    HeadingModule,
    MatIconModule,
    MatMenuModule,
    SelectorModule,
    ButtonModule,
    SwiperModule,
    CheckboxModule,
    PlayerModule,
  ],
})
export class ChannelsModule {}
