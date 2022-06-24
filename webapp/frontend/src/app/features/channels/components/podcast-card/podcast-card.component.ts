import { CardMenuEvents } from '@features/channels/values/card-menu-events.enum';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CardMenuItems } from '@features/channels/values/card-menu-items.const';

@Component({
  selector: 'podcast-card, [podcast-card]',
  templateUrl: './podcast-card.component.html',
  styleUrls: ['./podcast-card.component.scss'],
})
export class PodcastCardComponent {
  @Input() title: string;

  @Input() image: string;

  @Input() description: string;

  @Input() audioSource: string;

  @Output() menuItemClicked = new EventEmitter<CardMenuEvents>();

  readonly menuItems = CardMenuItems;

  get imageStyles() {
    return {
      backgroundImage: `url(${this.image})`,
    };
  }

  onClickMenu(event: CardMenuEvents) {
    this.menuItemClicked.emit(event);
    console.log(event);
  }
}
