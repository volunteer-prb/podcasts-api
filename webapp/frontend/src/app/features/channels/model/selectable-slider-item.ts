import { SliderItem } from './slider-item';

export interface SelectableSliderItem extends SliderItem {
  isSelected: boolean;
  index: number;
}
