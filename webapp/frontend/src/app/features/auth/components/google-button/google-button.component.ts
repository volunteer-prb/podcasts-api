import { ChangeDetectionStrategy, Component } from '@angular/core';

@Component({
  selector: 'google-button',
  templateUrl: './google-button.component.html',
  styleUrls: ['./google-button.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class GoogleButtonComponent {}
