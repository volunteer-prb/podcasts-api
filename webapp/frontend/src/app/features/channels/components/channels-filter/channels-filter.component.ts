import { Component, Input, ViewEncapsulation } from '@angular/core';
import { Channel } from '@features/channels/model/channel.model';
import { ChannelSelectValues } from 'src/app/__mocks__/channels';

@Component({
  selector: 'channels-filter',
  templateUrl: './channels-filter.component.html',
  styleUrls: ['./channels-filter.component.scss'],
  encapsulation: ViewEncapsulation.None,
})
export class ChannelsFilterComponent {
  readonly selectValues = ChannelSelectValues;

  @Input() channels: Channel[];
}
