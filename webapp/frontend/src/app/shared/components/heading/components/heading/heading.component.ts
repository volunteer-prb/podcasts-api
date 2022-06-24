import { ChangeDetectionStrategy, Component, Input } from '@angular/core';

@Component({
  selector: 'heading',
  templateUrl: './heading.component.html',
  styleUrls: ['./heading.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class HeadingComponent {
  @Input() title: string;
}
