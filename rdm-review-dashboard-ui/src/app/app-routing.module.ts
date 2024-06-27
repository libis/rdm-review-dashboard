import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SelectionListComponent } from "./selection-list/selection-list.component";
import { DatasetDetailComponent } from "./dataset-detail/dataset-detail.component";
import { DatasetFeedbackComponent } from "./dataset-feedback/dataset-feedback.component";
import { DatasetPublishComponent } from "./dataset-publish/dataset-publish.component";

const routes: Routes = [
  { path: "select", component: SelectionListComponent },
  { path: "datasets/:datasetId", component: DatasetDetailComponent },
  { path: "feedback/:datasetId", component: DatasetFeedbackComponent },
  { path: "publish/:datasetId", component: DatasetPublishComponent },
  { path: "", redirectTo: "/select", pathMatch: "full" },
  { path: "**", redirectTo: "/select" }
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { scrollPositionRestoration: 'enabled' })],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
