import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PaginationComponent } from './components/pagination/pagination.component';
import { NotFoundComponent } from './components/not-found/not-found.component';

@NgModule({
  declarations: [PaginationComponent, NotFoundComponent],
  imports: [CommonModule],
  exports: [PaginationComponent, NotFoundComponent],
})
export class SharedModule {}
