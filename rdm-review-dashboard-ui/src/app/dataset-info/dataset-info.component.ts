import { Component, OnInit, OnDestroy } from '@angular/core';
import { Dataset, DatasetContact } from '../models/dataset';
import { User } from '../models/user.model'
import { DialogService } from 'primeng/dynamicdialog';
import { MessageService } from 'primeng/api';
import { ReviewHistoryComponent } from '../review-history/review-history.component';
import { UserService } from '../services/user.service';
import { NoteTag } from '../models/note.model';
import { BehaviorSubject, Observable, Subscription, of, switchMap } from 'rxjs';
import { ReviewService } from '../services/review.service';
import { DatasetService } from '../services/dataset.service';
import { ApiService } from '../services/api.service';
import { AppConfigService } from '../services/app-config.service';

@Component({
  selector: 'app-dataset-info',
  templateUrl: './dataset-info.component.html',
  styleUrls: ['./dataset-info.component.scss'],
  providers: [DialogService, MessageService]

})
export class DatasetInfoComponent implements OnInit, OnDestroy {
  publishLock!: boolean;
  tags!: NoteTag[];
  supportTag$!: Observable<NoteTag[]>;
  departmentAndFacultyTags!: NoteTag[];
  tags$: Observable<NoteTag[]> = of([]);
  reviewerTags$!: Observable<NoteTag[]>;
  contributors: BehaviorSubject<User[]> = new BehaviorSubject<User[]>([]);
  datasetContact: BehaviorSubject<DatasetContact[]> = new BehaviorSubject<DatasetContact[]>([]);
  supportAsked: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
  dataset!: Dataset | null;
  tagsModified: BehaviorSubject<string> = new BehaviorSubject<string>(Date());
  reviewerDetails$!: Observable<User | null>;
  dataverseUrl: String;
  dataverseName: String;
  supportTagSubscription!: Subscription;
  datasetSubscription!: Subscription;
  contributorSubscription!: Subscription;
  contactSubscription!: Subscription;

  constructor(
    private dialogService: DialogService,
    public messageService: MessageService,
    public reviewService: ReviewService,
    public apiService: ApiService,
    public userService: UserService,
    public datasetService: DatasetService,
    private config: AppConfigService) {

    this.dataverseUrl = this.config.dataverseUrl;
    this.dataverseName = this.config.dataverseName;
  }


  ngOnInit(): void {
    this.tags = this.datasetService.getTags(this.dataset);
    this.reviewerTags$ = this.reviewService.selectedDataset.asObservable().pipe(
      switchMap((dataset) => this.datasetService.getReviewerTags(dataset)
      ));
      this.reviewService.update();
      this.datasetSubscription = this.reviewService.selectedDataset.asObservable().subscribe(
        (dataset) => { this.dataset = dataset; },
        (err) => { console.log(err) }
      )
      this.supportTag$ = this.reviewService.selectedDatasetId.asObservable().pipe(
        switchMap((datasetId) => {
          if (datasetId) { return this.apiService.retrieveSupportRequest(datasetId) }
          else {
            return of([])
          }
        }
        )
      )
      this.supportTagSubscription = this.supportTag$.subscribe(
        (tags) => {
          if (tags.length > 0) { this.supportAsked.next(true) }
          else { this.supportAsked.next(false) }
        }
      )
      
      this.reviewService.update();
      this.tags$ = this.reviewService.selectedDatasetTags$;
      this.contributorSubscription = this.reviewService.getContributor().subscribe(
        (contributors) => {
          this.contributors.next(contributors);
        }
      )
  
      this.contactSubscription = this.reviewService.getDatasetContact().subscribe(
        (datasetContact) => {
          this.datasetContact.next(datasetContact);
        }
      )
  }


  byteToGb(n: number): number {
    return n / Math.pow(1000, 3)
  }


  byteToMb(n: number): number {
    return n / Math.pow(1000, 2)
  }


  byteToKb(n: number): number {
    return n / Math.pow(1000, 1)
  }


  getDatasetSize() {
    if (!this.dataset?.size) {
      return '0 B'
    }
    let result = ''
    if (this.dataset.size < Math.pow(1000, 1)) {
      result = this.dataset.size.toFixed(2) + ' B'
    } else if (this.dataset.size < Math.pow(1000, 2)) {
      result = this.byteToKb(this.dataset.size).toFixed(2) + ' KB'
    } else if (this.dataset.size < Math.pow(1000, 3)) {
      result = this.byteToMb(this.dataset.size).toFixed(2) + ' MB'
    } else {
      result = this.byteToGb(this.dataset.size).toFixed(2) + ' GB'
    }
    return result;
  }


  updateTags() {
    this.tagsModified.next(Date.now().toString())
  }


  mailToContributors() {
    let names = [];
    let emails = [];
    for (let contributor of this.contributors.value) {
      names.push(contributor.userfirstname || contributor.name || contributor.username);
      emails.push(contributor.useremail);
    }
    let url = `mailto:${emails.join('; ')}?subject=Your dataset [${this.dataset?.identifier}]&Body=Dear ${names!.join(', ')},`
    window.open(url, "_top");
  }

  mailToContact() {
    let names = [];
    let emails = [];
    for (let contributor of this.datasetContact.value) {
      names.push(contributor.datasetContactName);
      emails.push(contributor.datasetContactEmail);
    }
    let url = `mailto:${emails.join('; ')}?subject=Your dataset [${this.dataset?.identifier}]&Body=Dear ${names!.join(', ')},`
    window.open(url, "_top");
  }

  openDataset() {
    /** 
     * Opens the dataset in a new tab.
     */
    if (this.dataset) {
      let url = `${this.dataverseUrl}/dataset.xhtml?persistentId=${this.dataset.identifier}`
      if (this.dataset.status == Dataset.Status.Draft || this.dataset.status == Dataset.Status.InReview || this.dataset.status == Dataset.Status.SubmittedForReview) {
        url += '&version=DRAFT'
      }
      window.open(url, "_blank");
    }
  }


  showReviewHistory() {
    const ref = this.dialogService.open(ReviewHistoryComponent, {
      header: `Review history for  \"${this.dataset?.title}\" `,
      width: '70%'
    }
    );
  }


  askSupport() {
    if (!this.dataset) {
      this.supportTag$ = of([]);
      return;
    }
    this.supportTag$ = this.apiService.askSupport(this.dataset.identifier).pipe(
      switchMap(tags => {
        if (tags.length > 0) { this.supportAsked.next(true) } else { this.supportAsked.next(false) };
        return of(tags)
      })
    );

  }


  removeSupport() {
    if (!this.dataset) {
      this.supportTag$ = of([]);
      return;
    }
    this.supportTag$ = this.apiService.removeSupportRequest(this.dataset.identifier).pipe(
      switchMap(tags => {
        if (tags.length > 0) { this.supportAsked.next(true) } else { this.supportAsked.next(false) };
        return of(tags)
      })
    );
  }

  ngOnDestroy(): void {
    this.datasetSubscription.unsubscribe();
    this.supportTagSubscription.unsubscribe();
    this.contactSubscription.unsubscribe();
    this.contributorSubscription.unsubscribe();
  }

}
