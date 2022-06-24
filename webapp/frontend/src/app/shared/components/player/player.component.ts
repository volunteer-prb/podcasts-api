import { PlayerService } from './services/player.service';
import { Subscription, fromEvent, filter, Observable } from 'rxjs';
import { AfterViewInit, Component, ElementRef, Input, OnDestroy, ViewChild } from '@angular/core';
import { AudioEvents } from './values/audio-events.enum';

@Component({
  selector: 'player',
  templateUrl: './player.component.html',
  styleUrls: ['./player.component.scss'],
  providers: [PlayerService],
})
export class PlayerComponent implements OnDestroy, AfterViewInit {
  private readonly subscriptions = new Subscription();

  private audio: HTMLAudioElement;

  @Input() source: string;

  @ViewChild('audio', { static: true }) private audioRef: ElementRef<HTMLAudioElement>;

  @ViewChild('track', { static: true }) private trackRef: ElementRef<HTMLElement>;

  isPlaying = false;

  private currentPercent = 0;

  get fillTrackStyles() {
    return {
      width: `${this.currentPercent}%`,
    };
  }

  get duration(): number {
    return this.playerService.duration ?? 0;
  }

  get currentTime$(): Observable<number> {
    return this.playerService.currentTime$;
  }

  constructor(private playerService: PlayerService) {}

  ngAfterViewInit() {
    this.audio = this.audioRef.nativeElement;

    this.subscriptions.add(
      fromEvent(this.audio, AudioEvents.LOADED_METADATA).subscribe(() => {
        this.playerService.duration = this.audio.duration;
      }),
    );

    this.subscriptions.add(
      fromEvent(this.audio, AudioEvents.PLAYING).subscribe(() => {
        this.playerService.setPlaying((this.isPlaying = true));
      }),
    );

    this.subscriptions.add(
      fromEvent(this.audio, AudioEvents.PAUSE).subscribe(() => {
        this.playerService.setPlaying((this.isPlaying = false));
      }),
    );

    this.subscriptions.add(
      fromEvent(this.audio, AudioEvents.TIMEUPDATE).subscribe(() => {
        this.playerService.setCurrentTime(this.audio.currentTime);
      }),
    );

    this.subscriptions.add(
      fromEvent(this.audio, AudioEvents.ENDED).subscribe(() => {
        this.seekTo(0);
        this.pause();
      }),
    );

    this.subscriptions.add(
      fromEvent(this.trackRef.nativeElement, 'click').subscribe((e: Event) => {
        const element = this.trackRef.nativeElement as HTMLElement;
        const event = e as PointerEvent;

        this.seekTo(this.playerService.getTimeFromPosition(event.offsetX, element.clientWidth));
      }),
    );

    this.subscriptions.add(
      this.playerService.currentPercent$
        .pipe(filter((value) => !!value))
        .subscribe((currentPercent) => {
          this.currentPercent = currentPercent;
        }),
    );
  }

  ngOnDestroy() {
    this.subscriptions.unsubscribe();
  }

  play() {
    this.audio.play();
  }

  pause() {
    this.audio.pause();
  }

  togglePlaying() {
    if (this.isPlaying) this.pause();
    else this.play();
  }

  seekTo(time: number) {
    this.audio.currentTime = Math.round(time);
  }
}
