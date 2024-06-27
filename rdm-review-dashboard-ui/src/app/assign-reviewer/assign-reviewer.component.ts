import { Component, OnInit, Input } from '@angular/core';
import { User } from '../models/user.model';
import { DynamicDialogRef } from 'primeng/dynamicdialog';
import { DynamicDialogConfig } from 'primeng/dynamicdialog';

@Component({
  selector: 'app-assign-reviewer',
  templateUrl: './assign-reviewer.component.html',
  styleUrls: ['./assign-reviewer.component.scss']
})
export class AssignReviewerComponent {
  selectedReviewer!: User;
  reviewers: User[] = [];

  constructor(public ref: DynamicDialogRef, public config: DynamicDialogConfig) {
    let reviewersReordered: User[] = [];
    for (let reviewer of this.config.data?.assignableReviewers || []) {
      if (this.config.data?.datasetReviewerIds.includes(reviewer.username)) {
        reviewersReordered.push(reviewer);
      } else if (reviewer.username == this.config.data?.currentUser) {
        this.reviewers.unshift(reviewer);
      } else {
        this.reviewers.push(reviewer);
      }
    }
    this.reviewers = reviewersReordered.concat(this.reviewers);
  }

  selectReviewer(reviewer: User) {
    this.ref.close(reviewer.username);
  }
}
