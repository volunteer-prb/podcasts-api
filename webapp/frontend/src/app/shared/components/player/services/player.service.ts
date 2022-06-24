import { Injectable } from '@angular/core';
import { BehaviorSubject, map, Observable } from 'rxjs';

@Injectable()
export class PlayerService {
  private _duration = 0;

  get duration(): number {
    return this._duration;
  }

  set duration(d: number) {
    this._duration = d;
  }

  private readonly playing = new BehaviorSubject(false);

  get playing$(): Observable<boolean> {
    return this.playing.asObservable();
  }

  setPlaying(isPlaying: boolean) {
    this.playing.next(isPlaying);
  }

  private readonly currentTime = new BehaviorSubject(0);

  get currentTime$() {
    return this.currentTime.asObservable();
  }

  setCurrentTime(time: number) {
    this.currentTime.next(time);
  }

  get currentPercent$(): Observable<number> {
    return this.currentTime$.pipe(map((time) => ((time ?? this.duration) / this.duration) * 100));
  }

  private getTimelinePercent(x: number, width: number) {
    return (x / width) * 100;
  }

  private getTimeFromPercent(totalTime: number, percent: number) {
    return (totalTime / 100) * percent;
  }

  getTimeFromPosition(x: number, width: number) {
    const percent = this.getTimelinePercent(x, width);

    console.log(this.getTimeFromPercent(this.duration, percent), 'getTimeFromPercent');

    return this.getTimeFromPercent(this.duration, percent);
  }
}
