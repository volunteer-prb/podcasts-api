import { SliderItem } from './slider-item.model';

export interface SelectableSliderItem extends SliderItem {
  isSelected: boolean;
  index: number;
}
