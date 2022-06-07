import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { NotFoundComponent } from '@shared/components/not-found/not-found.component';

const routes: Routes = [
  {
    path: '',
    loadChildren: () =>
      import('./features/welcome/welcome.module').then((m) => m.WelcomeModule),
  },
  {
    path: 'channels',
    loadChildren: () =>
      import('./features/channels/channels.module').then(
        (m) => m.ChannelsModule
      ),
  },
  { path: '**', component: NotFoundComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
