import { Component, OnInit, OnDestroy } from '@angular/core';
import { Pagination } from '@shared/core/pagination';
import { LoggerService } from '@shared/services/logger.service';
import { Subscription } from 'rxjs';
import { MockPodcastCards } from 'src/app/__mocks__/podcast-card';
import { SourceChannel } from './data/source-channel';
import { ChannelsService } from './services/channels.service';

@Component({
  selector: 'channels',
  templateUrl: './channels.component.html',
  styleUrls: ['./channels.component.scss'],
})
export class ChannelsComponent implements OnInit, OnDestroy {
  readonly mockCards = MockPodcastCards;

  private readonly subscriptions = new Subscription();

  pending: boolean = false;

  items: SourceChannel[] = [];

  pagination: Pagination = new Pagination();

  constructor(private channelsService: ChannelsService, private logger: LoggerService) {}

  ngOnInit() {
    this.load();
  }

  ngOnDestroy() {
    this.subscriptions.unsubscribe();
  }

  load() {
    this.pending = true;
    this.channelsService.find().subscribe(
      (data) => {
        this.pending = false;
        this.items = data.items;
        this.pagination = data.pagination;
      },
      (error) => {
        this.pending = false;
        this.logger.errorMessage('Error while loading channels', error?.error?.message);
      },
    );
  }

  // eslint-disable-next-line
  gotoPage(page: number) {
    this.logger.warn('Not implemented');
  }
}
