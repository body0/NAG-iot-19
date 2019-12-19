import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { StatisticComponent } from './statistic/statistic.component';
import { ActualStateComponent } from './actual-state/actual-state.component';

const routes: Routes = [
  { path: '', redirectTo: 'state', pathMatch: 'full' },
  { path: 'statistic', component: StatisticComponent },
  { path: 'state', component: ActualStateComponent },
  { path: '**', redirectTo: '' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
