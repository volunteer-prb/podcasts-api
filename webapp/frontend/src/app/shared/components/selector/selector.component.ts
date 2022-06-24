import { Component, EventEmitter, Input, Output, ViewEncapsulation } from '@angular/core';
import { Select } from './models/select.model';

@Component({
  selector: 'selector',
  templateUrl: './selector.component.html',
  styleUrls: ['./selector.component.scss'],
  encapsulation: ViewEncapsulation.None,
})
export class SelectorComponent {
  @Input() values: Select[];

  @Output() selectChange = new EventEmitter<Select>();

  onChange(value: Select) {
    this.selectChange.emit(value);
  }
}
