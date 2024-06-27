// Angular
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { APP_INITIALIZER } from '@angular/core';


// PrimeNG
import { StyleClassModule } from 'primeng/styleclass';
import { AvatarModule } from 'primeng/avatar';
import { BlockUIModule } from 'primeng/blockui';
import { ButtonModule } from "primeng/button";
import { CheckboxModule } from "primeng/checkbox";
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { EditorModule } from 'primeng/editor';
import { SplitButtonModule } from 'primeng/splitbutton';
import { DataViewModule } from 'primeng/dataview';
import { DialogModule } from 'primeng/dialog';
import { InputTextareaModule } from 'primeng/inputtextarea';
import { ListboxModule } from 'primeng/listbox';
import { DynamicDialogModule } from 'primeng/dynamicdialog';
import { DropdownModule } from 'primeng/dropdown';
import { PaginatorModule } from 'primeng/paginator';
import { ProgressBarModule } from 'primeng/progressbar';
import { ProgressSpinnerModule } from 'primeng/progressspinner';
import { RadioButtonModule } from 'primeng/radiobutton';
import { SkeletonModule } from 'primeng/skeleton';
import { TableModule } from 'primeng/table';
import { TabViewModule } from 'primeng/tabview';
import { TagModule } from "primeng/tag";
import { TooltipModule } from 'primeng/tooltip';


// App Modules
import { AppComponent } from './app.component';
import { AppConfigService } from './services/app-config.service';
import { AppRoutingModule } from './app-routing.module';
import { AssignButtonComponent } from './assign-button/assign-button.component';
import { AssignReviewerComponent } from './assign-reviewer/assign-reviewer.component';
import { AvatarComponent } from './avatar/avatar.component';
import { DatasetChecklistComponent } from './dataset-checklist/dataset-checklist.component';
import { DatasetDetailComponent } from './dataset-detail/dataset-detail.component';
import { DatasetFeedbackComponent } from './dataset-feedback/dataset-feedback.component';
import { DatasetInfoComponent } from './dataset-info/dataset-info.component';
import { DatasetPublishComponent } from './dataset-publish/dataset-publish.component';
import { DatasetTagsComponent } from './dataset-tags/dataset-tags.component';
import { ProgressSectionComponent } from './progress-section/progress-section.component';
import { ProgressItemComponent } from './progress-item/progress-item.component';
import { SelectionListComponent } from './selection-list/selection-list.component';
import { SelectionItemComponent } from './selection-item/selection-item.component';
import { TagComponent } from './tag/tag.component';
import { TopBannerComponent } from './top-banner/top-banner.component';

// 
import { ReviewHistoryComponent } from './review-history/review-history.component';


@NgModule({
  declarations: [
    AppComponent,
    AssignButtonComponent,
    AssignReviewerComponent,
    AvatarComponent,
    DatasetChecklistComponent,
    DatasetDetailComponent,
    DatasetFeedbackComponent,
    DatasetInfoComponent,
    DatasetPublishComponent,
    DatasetTagsComponent,
    ProgressItemComponent,
    ProgressSectionComponent,
    SelectionItemComponent,
    SelectionListComponent,
    TagComponent,
    TopBannerComponent,
    ReviewHistoryComponent],
  imports: [
    AppRoutingModule,
    AvatarModule,
    BrowserAnimationsModule,
    BrowserModule,
    BlockUIModule,
    ButtonModule,
    CheckboxModule,
    ConfirmDialogModule,
    DataViewModule,
    DialogModule,
    DropdownModule,
    DynamicDialogModule,
    EditorModule,
    FormsModule,
    HttpClientModule,
    InputTextareaModule,
    ListboxModule,
    PaginatorModule,
    ProgressBarModule,
    ProgressSpinnerModule,
    RadioButtonModule,
    ReactiveFormsModule,
    SkeletonModule,
    SplitButtonModule,
    StyleClassModule,
    TabViewModule,
    TableModule,
    TagModule,
    TooltipModule,
  ],
  entryComponents: [
    AssignReviewerComponent
  ],
  providers: [{
    provide: APP_INITIALIZER,
    multi: true,
    deps: [AppConfigService],
    useFactory: (appConfigService: AppConfigService) => {
      return () => {
        return appConfigService.loadConfig();
      };
    }
  }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
