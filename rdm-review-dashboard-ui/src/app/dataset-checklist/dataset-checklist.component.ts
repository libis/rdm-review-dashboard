import { Component, Input } from '@angular/core';
import { IssueDetail, ReviewService } from '../services/review.service';
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

  constructor(public reviewService: ReviewService) {
    this.reviewService.getSelectedDatasetIssues().subscribe(
      (issues) => {
        if (issues) {
          this.checklist = issues.manual_checklist;
          this.checklistCategories = issues.categories;
          for (let issue of issues.details) {
            this.issueDetails.set(issue.id, issue);
          }
        }
      }
    )
  }

  onChecklistChange() {
    this.reviewService.setCheckList(this.checklist);
  }

}
