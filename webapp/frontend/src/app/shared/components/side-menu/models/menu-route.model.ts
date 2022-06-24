import { AppRoutes } from '@core/values/app-routes.enum';
import { IconClass } from '@core/values/icon-class.enum';

export interface MenuRoute {
  title: string;
  iconClass: IconClass;
  route: AppRoutes[];
}
