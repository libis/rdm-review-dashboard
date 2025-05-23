import { Component, Input } from '@angular/core';
import { IssueDetail, ReviewService } from '../services/review.service';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-dataset-checklist',
  templateUrl: './dataset-checklist.component.html',
  styleUrls: ['./dataset-checklist.component.scss']
})
export class DatasetChecklistComponent {
  checklist: string[] = [];
  issueDetails: Map<string, IssueDetail> = new Map<string, IssueDetail>();
  @Input() datasetId!: string;
  issues!: any;
  checklistCategories: any[] = [];
  autoChecklist: Map<String, boolean | null> = new Map<String, boolean | null>();
  autoCheckWarnings: Map<String, String | null> = new Map<String, String | null>();
  lastAutocheck!: string | null;
  constructor(public reviewService: ReviewService, private datePipe: DatePipe) {
    this.reviewService.getSelectedDatasetIssues().subscribe(
      (issues) => {
        if (issues) {
          this.checklist = issues.manual_checklist;
          console.log(this.autoChecklist)
          this.checklistCategories = issues.categories;
          this.lastAutocheck = issues.autocheck_performed;
          for (let issue of issues.details) {
            this.issueDetails.set(issue.id, issue);
          }
          for (const [key, value] of Object.entries(issues.auto_checklist_states as { [key: string]: boolean | null })) {
            this.autoChecklist.set(key, value);
          }
          for (const [key, value] of Object.entries(issues.auto_checklist_messages as { [key: string]: String | null })) {
            this.autoCheckWarnings.set(key, value);
          }

        }
      }
    )
  }

  onChecklistChange() {
    this.reviewService.setCheckList(this.checklist);
  }

  getAutocheckState(item: String) {
    let result = this.autoChecklist.get(item);
    return result;
  }

  getAutocheckWarning(item: String): String | null | undefined {
    return this.autoCheckWarnings.get(item);
  }

  isDefaultAutocheckedState(item: string): boolean {

    if (!this.isAutochecksDone()) {
      return false;
    }

    if (this.checklist.includes(item) && this.getAutocheckState(item) == true) {
      return true;
    } else if (!this.checklist.includes(item) && this.getAutocheckState(item) != null && this.getAutocheckState(item) == false) {
      return true;
    }
    return false;
  }

  isAutochecksAvailable(): boolean {
    return true;
  }

  getLastAutocheck(): string | null {
    if (this.lastAutocheck == null) {
      return null;
    } else {
      return "Last checked: \n" + this.datePipe.transform(this.lastAutocheck, 'medium');
    }
  }

  isAutochecksDone(): boolean {
    return this.getLastAutocheck() != null;
  }
}
