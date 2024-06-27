import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, of, map } from 'rxjs';
import { Dataset, DatasetContact } from '../models/dataset';
import { User } from '../models/user.model';
import { ApiService } from './api.service';
import { DatasetService } from './dataset.service';
import { UserService } from './user.service';
import { AppConfigService } from './app-config.service';
import { HistoryItem, NoteTag } from '../models/note.model';


export interface IssueDetail {
  category: string;
  id: string;
  title: string;
  condition: string;
  message: string;
  warning: string;
}

export interface Warning {
  category: string;
  text: string;
}

@Injectable({
  providedIn: 'root'
})
export class ReviewService {
  selectedDatasetId: BehaviorSubject<string | null> = new BehaviorSubject<string | null>(null);
  selectedDataset: BehaviorSubject<Dataset | null> = new BehaviorSubject<Dataset | null>(null);
  selectedDatasetToBePublished = false;



  warnings: BehaviorSubject<Warning[]> = new BehaviorSubject<Warning[]>([]);

  selectedDatasetSavedFeedback: BehaviorSubject<string | null> = new BehaviorSubject<string | null>(null);
  selectedDatasetAutoGeneratedFeedback: BehaviorSubject<string | null> = new BehaviorSubject<string | null>(null);
  selectedDatasetSavedInternalNote: BehaviorSubject<string | null> = new BehaviorSubject<string | null>(null);

  selectedDatasetObservableTags$!: Observable<NoteTag[]>;
  selectedDatasetTags$!: Observable<NoteTag[]>;

  loggedUserIsReviewerOfSelectedDataset: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
  modified: BehaviorSubject<string> = new BehaviorSubject<string>(Date());
  supportAsked$!: Observable<boolean>;
  reviewerDetails: BehaviorSubject<User | null> = new BehaviorSubject<User | null>(null);


  constructor(private datasetService: DatasetService,
    private userService: UserService,
    private apiService: ApiService,
    private config: AppConfigService) {
    this.selectedDatasetId.next(null);

    let subscription = this.selectedDatasetId.asObservable().subscribe(
      {
        next: (datasetId) => {
          if (datasetId) {
            this.apiService.retrieveDatasetDetails(datasetId).subscribe(
              (dataset) => {
                if (dataset) {
                  this.selectedDataset.next(dataset);
                  this.apiService.retrieveFeedback(dataset.identifier).subscribe(
                    (feedback) => {
                      if (feedback.text != null) {
                        this.selectedDatasetSavedFeedback.next(feedback.text);
                      } else {
                        this.selectedDatasetSavedFeedback.next(null);
                      }
                    }
                  );
                  this.apiService.retrieveInternalNote(dataset.identifier).subscribe(
                    (notes) => {
                      this.selectedDatasetSavedInternalNote.next(notes.text);
                    }
                  );
                  this.update();
                } else {
                  this.selectedDataset.next(null);
                  this.update();
                }
              })
          }
        }
      });


    this.selectedDatasetTags$ = this.modified.asObservable().pipe(
      map(
        (modified) => this.datasetService.getTags(this.selectedDataset.value)
      )
    );


  }

  update() {
    this.modified.next(Date().valueOf());
  }

  delay(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  clearDatasets() {
    this.datasetService.clearDatasets();
  }

  updateDatasets() {
    this.datasetService.updateDatasets();
  }

  getSelectedDatasetIssues() {
    /** 
     * retrieves the issue report of the dataset, containing the definitions of the issues, automatic check results. 
     */
    let result = this.apiService.retrieveDatasetIssues(this.selectedDatasetId.value);
    return result;
  }

  setCheckList(values: string[]) {
    /**
     * stores the values of the dataset issues checklist, set by the user.  
     */
    if (this.selectedDatasetId.value) {
      this.apiService.updateDatasetIssuesChecklist(this.selectedDatasetId.value, values);
    }
  }


  getSelectedDatasetAutoGeneratedFeedback() {
    /** 
     * retrieves the issue report of the dataset, containing the definitions of the issues, automatic check results. 
     */
    let result = this.apiService.retrieveAutoGeneratedFeedback(this.selectedDatasetId.value || '');
    return result;
  }

  getSelectedDatasetFeedback(): string | null {
    return this.selectedDatasetSavedFeedback.value;
  }


  setFeedback(newFeedback: string | null) {
    if (this.selectedDataset.value) {

      this.apiService.updateFeedback(this.selectedDataset.value.identifier, newFeedback).subscribe(
        (result) => {
          this.selectedDatasetSavedFeedback.next(newFeedback);
        });
    }
  }


  getSelectedDatasetInternalNote(): string | null {

    return this.selectedDatasetSavedInternalNote.value;
  }

  setInternalNote(newNote: string) {
    if (this.selectedDataset.value) {


      this.apiService.updateInternalNote(this.selectedDataset.value.identifier, newNote).subscribe(
        (result) => {
          this.selectedDatasetSavedInternalNote.next(newNote);
        }
      );
    }

  }

  getTagByType(tags: any[] | null, type: string): string {
    if (tags) {
      for (let tag of tags) {
        if (tag.type == type) {
          return tag.content;
        }
      }
    }
    return '';
  }

  getHistory(): Observable<HistoryItem[]> {
    if (!this.selectedDataset.value) {
      return of([]);
    }
    return this.apiService.retrieveHistory(this.selectedDataset.value.identifier).pipe(
      map(
        (history) => {
          let result: HistoryItem[] = [];
          for (let item of history) {
            let newItem: HistoryItem = {
              userId: item.userId,
              created: item.created,
              text: item.text,
              category: this.getTagByType(item.tags, 'category'),
              subcategory: this.getTagByType(item.tags, 'subcategory')
            };
            result.push(newItem);
          }
          return result;
        }
      )
    )
  }

  publishSelected(version: string): Observable<Object> {
    return this.apiService.publishDataset(this.selectedDatasetId.value || '', version);
  }

  unAssignReviewer() {
    const subscription = this.apiService.unAssignReviewer(this.selectedDatasetId.value || '').subscribe(
      () => {
        subscription.unsubscribe();
      }
    )
  }

  updateLocks() {
    this.datasetService.updateDatasetsToPollLocksLists();
  }

  returnSelected() {
    if (this.selectedDatasetId.value) {
      let subscription = this.apiService.returnDataset(this.selectedDatasetId.value, this.selectedDatasetSavedFeedback.value).subscribe(
        {
          next: (response) => {
            this.delay(0).then(
              () => {
                this.clearDatasets();
                this.updateDatasets();
                subscription.unsubscribe();
              }
            )
          }
        }
      );
      return true;
    } else {
      return null;
    }
  }

  isLockedForReviewing() {
    if (this.selectedDatasetId.value) {
      return this.datasetService.isLockedForReviewing(this.selectedDatasetId.value);
    } else {
      return true;
    }
  }

  canLoggedUserReadSelectedDataset() {
    return this.userService.loggedUserId.value && 
      this.selectedDataset.value?.reviewer.includes(this.userService.loggedUserId.value) || this.userService.loggedUserDetails.value?.isAdmin;
  }


  getContributor() {
    if (this.selectedDatasetId.value) {
      return this.apiService.retrieveDatasetContributor(this.selectedDatasetId.value);
    } else {
      return of([]);
    }
  }

  getDatasetContact() :Observable<DatasetContact[]> {
    if (this.selectedDatasetId.value) {
      return this.apiService.retrieveDatasetContact(this.selectedDatasetId.value);
    } else {
      return of([]);
    }
  }

}

