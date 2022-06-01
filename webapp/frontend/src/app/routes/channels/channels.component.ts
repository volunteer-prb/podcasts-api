import { Component, OnInit } from '@angular/core';
import {ChannelsService} from "../../services/endpoints/channels.service";
import {SourceChannel} from "../../classes/model/source-channel";
import {Pagination} from "../../classes/core/pagination";
import {LoggerService} from "../../services/logger.service";

@Component({
  selector: 'app-channels',
  templateUrl: './channels.component.html',
  styleUrls: ['./channels.component.scss']
})
export class ChannelsComponent implements OnInit {

  pending: boolean = false
  items: SourceChannel[] = []
  pagination: Pagination = new Pagination()

  constructor(private channelsService: ChannelsService,
              private logger: LoggerService,
              ) { }

  ngOnInit(): void {
    this.load()
  }

  load() {
    this.pending = true
    this.channelsService.find().subscribe(data => {
      this.pending = false
      this.items = data.items
      this.pagination = data.pagination
    }, error => {
      this.pending = false
      this.logger.errorMessage('Error while loading channels', error?.error?.message)
    })
  }

  gotoPage(page: number) {
    this.logger.warn('Not implemented')
  }

}
