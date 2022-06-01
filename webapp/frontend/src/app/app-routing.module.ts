import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {ChannelsComponent} from "./routes/channels/channels.component";
import {WelcomeComponent} from "./routes/welcome/welcome.component";
import {NotFoundComponent} from "./routes/not-found/not-found.component";

const routes: Routes = [
  { path: '', component: WelcomeComponent },
  { path: 'channels', component: ChannelsComponent },
  { path: '**', component: NotFoundComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
