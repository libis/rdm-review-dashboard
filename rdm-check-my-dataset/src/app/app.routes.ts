import { RouterModule, Routes } from '@angular/router';
import { DatasetSelection } from './components/dataset-selection/dataset-selection';
import { NgModule } from '@angular/core';
import { Checklist } from './components/checklist/checklist';

export const routes: Routes = [
    {  path: "select", component: DatasetSelection },
    { path: "checklist/:datasetId", component: Checklist},
    { pathMatch: "full", path: "", redirectTo: "select"},
    { path: "**", redirectTo: "select"},
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { anchorScrolling: 'enabled', scrollPositionRestoration: 'enabled', useHash: true })],
  exports: [RouterModule],
})
export class AppRoutingModule {}
