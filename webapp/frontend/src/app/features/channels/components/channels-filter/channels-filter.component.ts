import { Component, ViewEncapsulation } from '@angular/core';
import { ChannelSelectValues, ChannelsList } from 'src/app/__mocks__/channels';

@Component({
  selector: 'channels-filter',
  templateUrl: './channels-filter.component.html',
  styleUrls: ['./channels-filter.component.scss'],
  encapsulation: ViewEncapsulation.None,
})
export class ChannelsFilterComponent {
  readonly selectValues = ChannelSelectValues;

  readonly channels = ChannelsList;
}
