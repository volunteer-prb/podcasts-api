import { CardMenuEvents } from './card-menu-events.enum';

export type CardMenuItem = {
  text: string;
  iconName: string;
  type: CardMenuEvents;
};

export const CardMenuItems: CardMenuItem[] = [
  {
    text: 'Редактировать',
    iconName: 'edit',
    type: CardMenuEvents.EDIT,
  },
  {
    text: 'Скачать',
    iconName: 'download',
    type: CardMenuEvents.DOWNLOAD,
  },
  {
    text: 'Перезалить',
    iconName: 'redo',
    type: CardMenuEvents.REUPLOAD,
  },
];
