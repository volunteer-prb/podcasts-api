import {
  ChangeDetectionStrategy,
  ChangeDetectorRef,
  Component,
  forwardRef,
  Input,
} from '@angular/core';
import { ControlValueAccessor, NG_VALUE_ACCESSOR } from '@angular/forms';

@Component({
  selector: 'input-field',
  templateUrl: './input-field.component.html',
  styleUrls: ['./input-field.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => InputFieldComponent),
      multi: true,
    },
  ],
})
export class InputFieldComponent implements ControlValueAccessor {
  @Input() placeholder: string = '';

  @Input() isInvalid = false;

  @Input() type: 'email' | 'password' | 'text' = 'email';

  value: string | undefined = '';

  isShowPassword = false;

  private onChange: (value: string) => void;

  private onTouched: () => void;

  constructor(private readonly changeDetector: ChangeDetectorRef) {}

  writeValue(value: string) {
    this.value = value;

    this.changeDetector.markForCheck();
  }

  registerOnChange(fn: (value: string) => void) {
    this.onChange = fn;
  }

  registerOnTouched(fn: () => void) {
    this.onTouched = fn;
  }

  onInputValueChange(event: Event) {
    const targetDivElement = event.target as HTMLInputElement;
    const value = targetDivElement.value;

    this.onChange(value);
  }

  togglePasswordVisibility() {
    this.isShowPassword = !this.isShowPassword;
  }
}
