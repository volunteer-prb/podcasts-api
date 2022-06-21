import { AppRoutes } from '@core/values/app-routes.enum';
import { IconClass } from '@core/values/icon-class.enum';
import { MenuRoute } from '../models/menu-route.model';

export const MenuRoutes: MenuRoute[] = [
  {
    title: 'Подкасты',
    iconClass: IconClass.MIRCO,
    route: [AppRoutes.ROOT, AppRoutes.CHANNELS],
  },
  {
    title: 'Настройки',
    iconClass: IconClass.SETTINGS,
    route: [AppRoutes.ROOT, AppRoutes.SETTINGS],
  },
];
