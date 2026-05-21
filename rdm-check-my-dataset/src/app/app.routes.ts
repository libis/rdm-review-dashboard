import { RouterModule, Routes } from '@angular/router';
import { DatasetSelection } from './components/dataset-selection/dataset-selection';
import { NgModule } from '@angular/core';
import { Checklist } from './components/checklist/checklist';

export const routes: Routes = [
    { pathMatch: "full", path: "select", component: DatasetSelection },
    { pathMatch: "full", path: "checklist/:datasetId", component: Checklist},
    { pathMatch: "full", path: "", redirectTo: "select"},
    { pathMatch: "full", path: "**", redirectTo: "select"},
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { anchorScrolling: 'enabled', scrollPositionRestoration: 'enabled', useHash: true })],
  exports: [RouterModule],
})
export class AppRoutingModule {}
