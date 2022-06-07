export class Pagination {
  hasNext: boolean = false;
  hasPrev: boolean = false;
  pageRange: number[] = [1];
  nextNum: number | undefined;
  prevNum: number | undefined;
  page: number = 1;

  static parser(obj: any): Pagination {
    const pag = new Pagination()
    if (obj === undefined || obj === null) {
      return pag
    }
    pag.hasPrev = obj.has_prev
    pag.pageRange = obj.page_range
    pag.hasNext = obj.has_next
    pag.nextNum = obj.next_num
    pag.prevNum = obj.prev_num
    pag.page = obj.page

    return pag
  }
}
