import { Component, OnInit } from '@angular/core';
import { Pagination } from '@shared/core/pagination';
import { LoggerService } from '@shared/services/logger.service';
import { SourceChannel } from '../data/source-channel';
import { ChannelsService } from '../services/channels.service';

@Component({
  selector: 'app-channels',
  templateUrl: './channels.component.html',
  styleUrls: ['./channels.component.scss'],
})
export class ChannelsComponent implements OnInit {
  pending: boolean = false;
  items: SourceChannel[] = [];
  pagination: Pagination = new Pagination();

  constructor(
    private channelsService: ChannelsService,
    private logger: LoggerService
  ) {}

  ngOnInit(): void {
    this.load();
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
        this.logger.errorMessage(
          'Error while loading channels',
          error?.error?.message
        );
      }
    );
  }

  gotoPage(page: number) {
    this.logger.warn('Not implemented');
  }
}
