import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Pagination } from '@shared/core/pagination';

@Component({
  selector: 'app-pagination',
  templateUrl: './pagination.component.html',
  styleUrls: ['./pagination.component.scss'],
})
export class PaginationComponent {
  @Input() pagination: Pagination = new Pagination();

  @Output() getPage: EventEmitter<{ page: number }> = new EventEmitter<{
    page: number;
  }>();

  public previousPage(): void {
    let page = this.pagination.page;
    this.getPage.emit({
      page: page - 1,
    });
  }

  public nextPage(): void {
    let page = this.pagination.page;
    this.getPage.emit({
      page: page + 1,
    });
  }

  goPage(page: number): void {
    this.getPage.emit({
      page: page,
    });
  }
}
