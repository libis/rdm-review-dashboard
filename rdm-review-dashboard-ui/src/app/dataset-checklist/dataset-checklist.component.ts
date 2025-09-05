import { Component, Input } from '@angular/core';
import { IssueDetail, ReviewService } from '../services/review.service';
import { DatePipe } from '@angular/common';
import { BehaviorSubject } from 'rxjs';
import { ColdObservable } from 'rxjs/internal/testing/ColdObservable';

@Component({
  selector: 'app-dataset-checklist',
  templateUrl: './dataset-checklist.component.html',
  styleUrls: ['./dataset-checklist.component.scss']
})
export class DatasetChecklistComponent {
  checklist: string[] = [];
  issueDetails: Map<string, IssueDetail> = new Map<string, IssueDetail>();
  @Input() datasetId!: string;
  checklistCategories: any[] = [];
  autoChecklist: Map<string, boolean | null> = new Map<string, boolean | null>();
  autoCheckWarnings: Map<string, string | null> = new Map<string, string | null>();
  lastAutocheck!: string | null;
  autochecksEnabled: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
  allSameAsAutocheck: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
  autoCheckSuccess: BehaviorSubject<boolean|null> = new BehaviorSubject<boolean|null>(null);
  autochecksAvailable: boolean = false;
  constructor(public reviewService: ReviewService, private datePipe: DatePipe) {
    this.reviewService.getSelectedDatasetIssues().subscribe(
      (issues) => {
        this.updateChecklist(issues);
        this.autochecksAvailable = issues.autochecks_available != null && issues.autochecks_available > 0;
      }
    )
  }
  allChecksSameAsAutocheck() {
    for (let issueName of this.issueDetails.keys()) {
      if (this.autoChecklist.get(issueName) === undefined || this.autoChecklist.get(issueName) === null) {
        continue;
      } else if (this.autoChecklist.get(issueName) === this.checklist.includes(issueName)) {
        continue;
      }
      else {
        return false;
      }
    }
    return true;

  }
  onChecklistChange() {
    let values: Map<string, boolean | null> = new Map<string, boolean | null>();
    for (let value of this.checklist) {
      values.set(value, true);
    }
    this.reviewService.setCheckList(values);
    this.allSameAsAutocheck.next(this.allChecksSameAsAutocheck());
  }

  runAutochecks() {
    this.autochecksEnabled.next(false);
    this.autoCheckSuccess.next(null);
    this.reviewService.runAutochecks().subscribe(
      {
        next: (autochecks) => this.updateChecklist(autochecks),
        error: (err) => {
          this.autochecksEnabled.next(true);
          this.lastAutocheck = null;
          this.autoCheckSuccess.next(false);
          console.log(err);
        }
      }
    );
  }

  getAutocheckState(item: string) {
    let result = this.autoChecklist.get(item);
    return result;
  }

  getAutocheckWarning(item: string): string | null | undefined {
    return this.autoCheckWarnings.get(item);
  }

  isDefaultAutocheckedState(item: string): boolean {

    if (this.lastAutocheck !== null) {
      return false;
    }

    if (this.checklist.includes(item) && this.getAutocheckState(item) === true) {
      return true;
    } else if (!this.checklist.includes(item) && this.getAutocheckState(item) != null && this.getAutocheckState(item) == false) {
      return true;
    }
    return false;
  }

  getAutocheckTooltip(): string | null {
    if (this.lastAutocheck === null && this.autoCheckSuccess.value !== false) {
      return 'Not checked';
    } else if (this.autoCheckSuccess.value === true) {
      return "Last checked: \n" + this.datePipe.transform(this.lastAutocheck, 'medium');
    } else if (this.autoCheckSuccess.value === false) {
      return "Last autocheck failed. Please try again.";
    } else {
      return null;
    }
  }

  getAutocheckButtonClass(): string {
    if (this.autoCheckSuccess.value === true) {
      return this.lastAutocheck != null ? 'p-button p-button-info p-button-outlined' : 'p-button p-button-info';
    } else if (this.autoCheckSuccess.value === false) {

      return 'p-button p-button-danger';
    } else {
      return 'p-button p-button-info';
    }
  }

  updateChecklist(issues: any) {
    if (issues) {
      this.checklistCategories = issues.categories;
      this.lastAutocheck = issues.autocheck_performed;
      this.autoCheckSuccess.next(true);
      for (let issue of issues.details) {
        this.issueDetails.set(issue.id, issue);
        if (issues.manual_checklist[issue.id]) {
          this.checklist.push(issue.id);
        }
      }
      for (const [key, value] of Object.entries(issues.auto_checklist_states as { [key: string]: boolean | null })) {
        this.autoChecklist.set(key, value);
      }
      for (const [key, value] of Object.entries(issues.auto_checklist_messages as { [key: string]: string | null })) {
        this.autoCheckWarnings.set(key, value);
      }
      this.autochecksEnabled.next(true);

    }
    this.allSameAsAutocheck.next(this.allChecksSameAsAutocheck());
  }
  updateFromAutochecks() {
    let checklist = [];
    for (let issuename of this.autoChecklist.keys()) {
      let currentIssue = this.autoChecklist.get(issuename);
      if (currentIssue == true || (this.checklist.includes(issuename) && currentIssue != false)) {
        checklist.push(issuename)
      }
    }
    this.checklist = checklist;
    this.allSameAsAutocheck.next(this.allChecksSameAsAutocheck());

  }
}
