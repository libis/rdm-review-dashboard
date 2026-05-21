import { Component, computed, OnInit, signal, Signal } from '@angular/core';
import { BehaviorSubject, map, combineLatest } from 'rxjs';
import { ChecklistItem } from '../checklist-item/checklist-item';
import { AccordionModule } from 'primeng/accordion';
import { ButtonModule } from 'primeng/button';
import { ActivatedRoute, Router } from '@angular/router';
import { ProgressSpinnerModule } from 'primeng/progressspinner';
import { DatasetService } from '../../services/dataset.service';
import { ApiService } from '../../services/api-service';
import { Config } from '../../services/config';
import { CardModule } from 'primeng/card';
import { AvatarModule } from 'primeng/avatar';
import { ProgressBarModule } from 'primeng/progressbar';
import { TaskStatus } from '../task-status/task-status';
import { TaskService } from '../../services/task-service';
import { DividerModule } from 'primeng/divider';
import { SpeedDialModule } from 'primeng/speeddial';
import { MenuItem, MessageService } from 'primeng/api';

@Component({
  selector: 'app-checklist',
  imports: [
    AvatarModule,
    CardModule,
    ChecklistItem,
    AccordionModule,
    DividerModule,
    ButtonModule,
    ProgressSpinnerModule,
    ProgressBarModule,
    TaskStatus,
    SpeedDialModule,
  ],
  templateUrl: './checklist.html',
  styleUrl: './checklist.scss',
  providers: [MessageService],
})
export class Checklist implements OnInit {
  datasetId: BehaviorSubject<string | null> = new BehaviorSubject<string | null>(null);
  checklistStatuses: string[] = [];
  allTasksDone: Signal<boolean> = signal(false);
  taskCategories: Signal<any[]> = signal([]);
  ForDataset: Signal<boolean | null> = signal(null);
  items: MenuItem[] | null = null;
  helpDeskEmail: string;
  dataverseName: string;
  supportLink: string;
  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private dataset: DatasetService,
    private api: ApiService,
    private tasks: TaskService,
    private config: Config,
  ) {
    combineLatest([this.route.params])
      .pipe(
        map((params: any) => {
          if (this.datasetId.value !== params[0]['datasetId']) {
            this.datasetId.next(params[0]['datasetId']);
            return params[0]['datasetId'];
          }
          return null;
        }),
      )
      .subscribe({
        next: (datasetId) => {
          if (typeof datasetId === 'string') {
            this.tasks.setTaskToFollow(datasetId);
            this.dataset.retrieve(datasetId);
          }
        },
      });
    this.allTasksDone = computed(
      () =>
        this.tasks.all().length >= 0 &&
        this.tasks.done().length >= 0 &&
        this.tasks.done().length == this.tasks.all().length,
    );
    this.taskCategories = computed(() => this.tasks.taskStatuses()?.structure);
    this.helpDeskEmail = this.config.helpDeskEmail;
    this.dataverseName = this.config.dataverseName;
    this.supportLink = this.config.supportLink;
  }

  ngOnInit() {
    this.items = [
      {
        label: 'Contact Helpdesk',
        tooltip: 'Contact Helpdesk',
        icon: 'pi pi-question',
        command: () => {
    window.open(
      `mailto:${this.helpDeskEmail}?subject=[Check-My-Dataset Review] (${this.getDatasetDOI()})`, "_top");
        },
      },
      {
        label: 'Support & Guidelines',
        tooltip: 'Support & Guidelines',
        icon: 'pi pi-book',
        command: () => {
          window.open(this.supportLink, "_blank");
        },
      },
    ];
  }

  pollResults(datasetId: string) {
    return this.api.pollResults(datasetId);
  }

  getIssueDetails(itemId: string) {
    return this.tasks.taskDescription().get(itemId);
  }

  hasTip(issueId: string) {
    return this.getIssueDetails(issueId).tip && this.getIssueDetails(issueId).tip !== '';
  }

  getTaskCompletionData(taskId: string) {
    let result = this.tasks.taskStatuses().tasks.find((item: any) => item.task_id === taskId);
    if (result === undefined) {
      return null;
    }
    return result;
  }

  getDatasetUrl() {
    let url = this.dataset.getDatasetUrl();
    if (!url?.includes('&version=DRAFT')) {
      url = url + '&version=DRAFT';
    }
    return url;
  }

  getTaskResults(taskId: string) {
    return this.tasks.results().get(taskId)?.results;
  }

  getTaskStatus(taskId: string) {
    return this.tasks.statuses().get(taskId);
  }

  getCompletionStatus(taskId: string) {
    return this.getTaskCompletionData(taskId)?.status || null;
  }

  isTaskDone(issueId: string): boolean {
    return (
      this.getCompletionStatus(issueId) !== null && this.getCompletionStatus(issueId) === 'done'
    );
  }

  hasTaskResults(issueId: string): boolean {
    let results = this.getTaskResults(issueId);
    if (results === undefined) {
      return false;
    }
    return results.result !== null || results.warning !== null || results.message !== null;
  }

  hasTaskFeedback(issueId: string): boolean {
    let results = this.getTaskResults(issueId);
    if (results === undefined) {
      return false;
    }
    return results.result === false || results.warning !== null || results.message !== null;
  }

  hasTaskTip(issueId: string): boolean {
    let results = this.getTaskResults(issueId);
    if (results === undefined) {
      return false;
    }
    return results.result === null || results.warning === null;
  }

  hasAutocheckResultToDisplay() {
    return this.tasks.all().some((task) => this.hasTaskResults(task.task_id));
  }

  getAutocheckAvailable(itemId: string) {
    let result = this.tasks
      .taskStatuses()
      .autochecks_available.find((item: any) => item.name === itemId);
    if (result === undefined) {
      return null;
    }
    return result;
  }

  isLargeDataset() {
    return true;
    return this.getTaskResults('totalDatasetFilesSizeIsLessThan5GB').result === false;
  }

  isLargeNumFiles() {
    return true;

    return this.getTaskResults('numFilesIsLessThan1000').result === false;
  }

  isFileSizeCheckFailed() {
    return this.isLargeDataset() || this.isLargeNumFiles();
  }

  getHelptext(itemId: string) {
    let autocheckInfo = this.getAutocheckAvailable(itemId);
    if (autocheckInfo !== null && autocheckInfo.helpText != null) {
      return autocheckInfo.helpText;
    }
    return null;
  }

  getDatasetTitle() {
    return this.dataset.dataset()?.title;
  }

  getDatasetDOI() {
    return this.dataset.dataset()?.identifier;
  }

  onClickNext() {
    this.router.navigate(['feedback', this.datasetId.value]);
  }

  hasCategoryActiveIssues(category: any) {
    console.log(category);
    if (category.issues.length == 0) {
      return false;
    }
    for (let issueID of category.issues) {
      console.log(category.label, issueID);
      if (this.isTaskDone(issueID) && this.hasTaskFeedback(issueID)) {
        return true;
      }
    }
    return false;
  }
}
