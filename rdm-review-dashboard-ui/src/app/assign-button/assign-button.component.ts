import { Component, OnInit, Input } from '@angular/core';
import { Dataset } from '../models/dataset';
import { UserService } from '../services/user.service';
import { DatasetService } from '../services/dataset.service';
import { AssignReviewerComponent } from '../assign-reviewer/assign-reviewer.component';
import { DialogService } from 'primeng/dynamicdialog';
import { MessageService } from 'primeng/api';
import { ConfirmationService } from 'primeng/api';
import { Router } from '@angular/router';
import { User } from '../models/user.model';

@Component({
  selector: 'app-assign-button',
  templateUrl: './assign-button.component.html',
  styleUrls: ['./assign-button.component.scss'],
  providers: [DialogService, MessageService, ConfirmationService]
})
export class AssignButtonComponent implements OnInit {
  constructor(public userService: UserService,
    private datasetService: DatasetService,
    private dialogService: DialogService,
    public messageService: MessageService,
    private confirmationService: ConfirmationService,
    private router: Router
  ) {
  }
  @Input() dataset!: Dataset;
  displayUnassign: boolean = false;
  isLockedForReviewing: boolean = false;

  ngOnInit(): void {
    this.isLockedForReviewing = this.datasetService.isLockedForReviewing(this.dataset.identifier);
  }

  isInReview(): boolean {
    /** 
     * Returns if the dataset is already in review. 
     */
    const result = this.dataset.status == Dataset.Status.InReview;
    return result;
  }


  isSubmittedForReview(): boolean {
    /**
     * Returns if the dataset is in 'Submitted for Review' status.
     */
    const result = this.dataset.status == Dataset.Status.SubmittedForReview;
    return result
  }


  canUnassignReviewer(): boolean {
    /** 
    * Returns if the reviewer can be unassigned from this dataset.
    * 'true' if the dataset is currently under review and the current user is assigned to this dataset as reviewer. 
    */
    const result = this.dataset.status == Dataset.Status.InReview && this.dataset.reviewer.includes(this.userService.loggedUserId.value || ' ');

    return result

  }


  getAssignableReviewers() {
    /**
     * Returns a list containing the list of users that can be assigned to the dataset by the currently logged user. 
     * If a user is 'reviewer' then they can only assign themselves. 
     * If a user is 'admin' then then they can assign themselves and other reviewers to the dataset. 
     */
    let possibleReviewers = this.userService.reviewers.value;
    let result: User[] = [];
    if (this.userService.loggedUserDetails.value?.isAdmin) {
      result = possibleReviewers;
    } else if (this.userService.loggedUserDetails.value?.isReviewer) {
      result = possibleReviewers.filter((reviewer) => reviewer.username == this.userService.loggedUserId.value);
    }
    return result;
  }


  showAssignDialogue() {
    /** 
     * Displays the dialog allowing selection of reviewer for the dataset by the currently logged user. 
     * If the user is not an 'admin' but a 'reviewer', the list will only contain the logged user. 
     */
    this.displayUnassign = true;

    const ref = this.dialogService.open(AssignReviewerComponent, {
      data: {
        datasetReviewerIds: this.dataset.reviewer,
        currentUser: this.userService.loggedUserId.value,
        assignableReviewers: this.getAssignableReviewers()
      },
      header: `Select reviewer for  \"${this.dataset.title}\" `,
      width: '70%'
    });
    let subscription = ref.onClose.subscribe((reviewer: any) => {
      if (reviewer) {
        this.datasetService.assignReviewerToDataset(this.dataset.identifier, reviewer);
        if (reviewer == this.userService.loggedUserId.value) {
          this.router.navigate(['/details']).then(() => { subscription.unsubscribe() });
        } else {
          this.router.navigate(['/select']).then(() => { subscription.unsubscribe() });
        }
      }
    }
    );
  }


  showUnassignDialog() {
    /**
     * Shows the dialog for unassigning from a dataset. 
     */
    this.confirmationService.confirm(
      {
        message: `Unassign dataset from ${this.dataset.reviewer}?`,
        accept: () => {
          this.datasetService.unAssignReviewerFromDataset(this.dataset.identifier);
          this.router.navigate(['/select']).then();

        }
      }
    );
  }
}
