import { ChangeDetectionStrategy, Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'checkbox',
  templateUrl: './checkbox.component.html',
  styleUrls: ['./checkbox.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class CheckboxComponent {
  @Input() isRound = false;

  @Output() checked = new EventEmitter<boolean>();

  onChange(event: Event) {
    const element = event.target as HTMLInputElement;

    this.checked.emit(element.checked);
  }
}
