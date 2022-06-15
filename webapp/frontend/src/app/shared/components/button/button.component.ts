import { Component, Input } from '@angular/core';
import { CssStyles } from '@core/types/css-styles.type';

@Component({
  selector: 'app-button',
  templateUrl: './button.component.html',
  styleUrls: ['./button.component.scss'],
})
export class ButtonComponent {
  @Input() disabled: boolean;

  @Input() width: number | string;

  @Input() height: number;

  @Input() type: 'fill' | 'outline' = 'fill';

  get styles(): CssStyles {
    return {
      width: typeof this.width === 'string' ? this.width : `${this.width}px`,
      height: `${this.height}px`,
    };
  }
}
