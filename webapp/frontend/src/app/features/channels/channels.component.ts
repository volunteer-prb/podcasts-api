import { ChannelsList } from 'src/app/__mocks__/channels';
import { Component } from '@angular/core';
import { MockPodcastCards } from 'src/app/__mocks__/podcast-card';

@Component({
  selector: 'channels',
  templateUrl: './channels.component.html',
  styleUrls: ['./channels.component.scss'],
})
export class ChannelsComponent {
  readonly mockCards = MockPodcastCards;

  readonly mockChannelsList = ChannelsList;
}
