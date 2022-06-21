import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from '@features/auth/guards/auth.guard';
import { NotFoundComponent } from '@shared/components/not-found/not-found.component';
import { AppRoutes } from './core/values/app-routes.enum';

const routes: Routes = [
  {
    path: '',
    pathMatch: 'full',
    redirectTo: AppRoutes.CHANNELS,
  },
  {
    path: AppRoutes.AUTH,
    loadChildren: () => import('./features/auth/auth.module').then((m) => m.AuthModule),
    data: {
      hasMenu: false,
    },
  },
  {
    path: AppRoutes.CHANNELS,
    canActivate: [AuthGuard],
    loadChildren: () => import('./features/channels/channels.module').then((m) => m.ChannelsModule),
  },
  {
    path: '**',
    component: NotFoundComponent,
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
