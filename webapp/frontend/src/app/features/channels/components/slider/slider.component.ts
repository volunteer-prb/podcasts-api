import {
  AfterViewInit,
  Component,
  ViewChild,
  ViewEncapsulation,
  OnDestroy,
  Input,
  OnInit,
  Output,
  EventEmitter,
} from '@angular/core';
import { Subscription } from 'rxjs';
import { SwiperComponent } from 'swiper/angular';
import Swiper from 'swiper';
import { SliderItem } from '@features/channels/model/slider-item';
import { SelectableSliderItem } from '@features/channels/model/selectable-slider-item';

@Component({
  selector: 'slider',
  templateUrl: './slider.component.html',
  styleUrls: ['./slider.component.scss'],
  encapsulation: ViewEncapsulation.None,
})
export class SliderComponent implements OnInit, AfterViewInit, OnDestroy {
  @Input() items: SliderItem[];

  @Output() selectItem = new EventEmitter<SliderItem>();

  selectableItems: SelectableSliderItem[];

  @ViewChild(SwiperComponent, { static: false })
  private swiper: SwiperComponent;

  private readonly subscriptions = new Subscription();

  private readonly TRANSITION = 100;

  private readonly FIRST_SLIDER_ITEM: SelectableSliderItem = {
    title: 'Все',
    index: 0,
    isSelected: true,
  };

  isShowControl = {
    left: false,
    right: true,
  };

  ngOnInit() {
    this.selectableItems = this.getSelectableItems(this.items, this.FIRST_SLIDER_ITEM);
  }

  ngAfterViewInit() {
    this.subscriptions.add(this.swiper.s_transitionStart.subscribe(this.setControlsVisibility));
  }

  ngOnDestroy() {
    this.subscriptions.unsubscribe();
  }

  private setControlsVisibility = ([swiper]: [Swiper]) => {
    this.isShowControl = {
      left: swiper.activeIndex !== 0,
      right: !swiper.isEnd,
    };
  };

  private getSelectableItems(
    items: SliderItem[],
    firstItem: SelectableSliderItem,
  ): SelectableSliderItem[] {
    return [firstItem, ...items].map((item, index) => {
      return {
        isSelected: false,
        index,
        ...item,
      };
    });
  }

  private changeSelect({ index }: SelectableSliderItem) {
    this.selectableItems.forEach((item, idx) => {
      if (index !== idx) {
        item.isSelected = false;
        return;
      }

      item.isSelected = true;
    });
  }

  nextSlide() {
    this.swiper.swiperRef.slideNext(this.TRANSITION);
  }

  prevSlide() {
    this.swiper.swiperRef.slidePrev(this.TRANSITION);
  }

  select(item: SelectableSliderItem) {
    this.changeSelect(item);
    this.selectItem.emit(item);
  }

  initSwipe([swiper]: [Swiper]) {
    setTimeout(() => {
      this.isShowControl.right = swiper.allowSlideNext;
    });
  }
}
