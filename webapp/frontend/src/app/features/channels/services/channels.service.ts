import { Injectable } from '@angular/core';

import { Observable } from 'rxjs';
import { RestService } from '@shared/services/communication/rest.service';
import { SourceChannel } from '../data/source-channel';
import { Pagination } from '@shared/core/pagination';

@Injectable({
  providedIn: 'root',
})
export class ChannelsService {
  constructor(private readonly rest: RestService) {}

  find(): Observable<{ items: SourceChannel[]; pagination: Pagination }> {
    return new Observable((subscriber) => {
      subscriber.next({
        items: [new SourceChannel(), new SourceChannel(), new SourceChannel()],
        pagination: Pagination.parser({
          has_prev: true,
          page_range: [1, 2, 3],
          has_next: true,
          next_num: 3,
          prev_num: 1,
          page: 2,
        }),
      });
    });
  }

  get(id: number): Observable<SourceChannel | undefined> {
    return new Observable<SourceChannel | undefined>((subscriber) => {
      subscriber.next(undefined);
    });
  }
}
