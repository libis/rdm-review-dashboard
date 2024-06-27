import {Component, Input, OnInit} from '@angular/core';
import {Dataset} from "../models/dataset";
import {User} from '../models/user.model'
import {Router} from "@angular/router";
import {DatasetService} from "../services/dataset.service";
import { ReviewService } from '../services/review.service';
import { UserService } from '../services/user.service';
import { Observable } from 'rxjs';
import { NoteTag } from '../models/note.model';


@Component({
  selector: 'div[app-selection-item]',
  templateUrl: './selection-item.component.html',
  styleUrls: ['./selection-item.component.scss']
})
export class SelectionItemComponent implements OnInit {

  @Input() dataset!: Dataset;
  departmentAndFacultyTags: NoteTag[] = [];
  staticTags: NoteTag[] = [];
  observableTags$!: Observable<NoteTag[]>;
  locked: boolean = true;
  reviewerTags$!: Observable<NoteTag[]>;
  reviewer!: User|null;

  constructor(private router: Router, 
    public datasetService: DatasetService, 
    public userService: UserService,
    private reviewService: ReviewService
    ) {
        this.reviewer = this.userService.assignableReviewers.value.find((reviewer)=>this.dataset.reviewer.includes(reviewer?.username || '')) || null;

      }

  ngOnInit(): void {
    this.staticTags = this.datasetService.getTags(this.dataset)
    this.departmentAndFacultyTags = this.datasetService.getDepartmentAndFacultyTags(this.dataset);
    this.observableTags$ = this.datasetService.getTagsAsObservable(this.dataset);
    this.reviewerTags$ = this.datasetService.getReviewerTags(this.dataset);
    this.locked = this.datasetService.isLockedForReviewing(this.dataset.identifier);
  }

  getClass(): string {
    if (!this.locked) {
      return "selection-item border-1 border-300 border-round pt-3 pb-5 pl-3 pr-3 shadow-3 surface-card h-full"
    } else {
      return "selection-item border-1 border-300 border-round pt-3 pb-5 pl-3 pr-3 shadow-3 surface-card h-full"
    }
  }

  getReviewButtonText(): string {
    return (this.dataset.status == Dataset.getStatus('in_review') && this.userService.loggedUserId.value && this.dataset.reviewer.includes(this.userService.loggedUserId.value)) ? "Review" : "View details" 
  }

  getButtonClass(button: string): string {
    if (button=='details') {
        if (this.dataset.status ==  Dataset.getStatus('in_review') && (this.dataset.reviewer.length == 0) && (this.userService.loggedUserDetails.value?.isAdmin || this.userService.loggedUserDetails.value?.isReviewer))  {
        return "flex-1 p-button-outlined p-2 m-2 align-items-center justify-content-center";
    }
  }
    return "flex-1 p-2 m-2 align-items-center justify-content-center"; 
  }
  viewDataset() {
    if (this.dataset) {
      this.reviewService.selectedDatasetId.next(this.dataset.identifier);
      this.router.navigate(['datasets', this.dataset.identifier]).then();
    }
  }
}
