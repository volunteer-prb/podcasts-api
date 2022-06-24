import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'minuteSeconds',
})
export class MinuteSecondsPipe implements PipeTransform {
  transform(value: number | null): string {
    if (!value) return '00:00';

    const minutes = Math.floor(Math.round(value) / 60);
    const seconds = value - minutes * 60;

    return this.prepareToString(minutes) + ':' + this.prepareToString(seconds);
  }

  private prepareToString(num: number): string {
    return num.toFixed(0).toString().padStart(2, '0');
  }
}
