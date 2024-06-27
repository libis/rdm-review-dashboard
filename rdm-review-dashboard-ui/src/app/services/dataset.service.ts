import { Injectable } from '@angular/core';
import { Dataset, DatasetCount } from "../models/dataset";
import { ApiService } from "./api.service";
import { BehaviorSubject, combineLatest, map, Observable, of, shareReplay, Subscription, switchMap } from "rxjs";
import { UserService } from './user.service';
import { NoteTag } from '../models/note.model';
import { interval } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DatasetService {

  datasets$!: Observable<Dataset[]>;

  modified: BehaviorSubject<string> = new BehaviorSubject<string>(Date());
  datasetLocks: BehaviorSubject<any> = new BehaviorSubject<any>({});
  datasetsToPollLocks: Set<string> = new Set<string>([]);

  datasetCount$!: Observable<DatasetCount[]>;
  loggedUserDatasetCount$!: Observable<DatasetCount[]>;

  constructor(
    private apiService: ApiService,
    private userService: UserService) {


    // total number of all datasets 
    this.datasetCount$ = this.modified.asObservable().pipe(
      switchMap(
        (modified) => {
          let result = this.apiService.retrieveDatasetStatusCount(null);
          return result;
        }

      ),
      shareReplay(1)
    )

    // total number of datasets assigned to the logged user. 
    this.loggedUserDatasetCount$ = combineLatest([
      this.modified.asObservable(),
      this.userService.loggedUserId.asObservable()])
      .pipe(
        switchMap(
          ([modified, userId]) => {
            if (userId) {

              let result = this.apiService.retrieveDatasetStatusCount(userId);
              return result;
            } else {
              return of([]);
            }
          }
        ),
        shareReplay(1)

      )


    let lockPollingSubscription = interval(2000).subscribe(
      () => {
        if (this.datasetsToPollLocks.size != 0) {
          this.pollDatasetsForLocks();
        }
      }
    )
  }



  getDatasetLocks(datasetId: string): String[] {
    /**
     * Returns the locks 
     */
    let result: string[] = []
    if (datasetId) {
      let locks = this.datasetLocks.value[datasetId];
      if (locks) {
        result = locks;
      }
    }
    return result;
  }

  isLockedForReviewing(datasetId: string): boolean {
    let locks = this.getDatasetLocks(datasetId);
    let locksForReviewing = ['Ingest', 'Workflow', 'DcmUpload', 'finalizePublication', 'EditInProgress', 'FileValidationFailed', "publishing"]
    for (let lock of locksForReviewing) {
      if (locks.includes(lock)) {
        return true
      }
    }
    return false
  }


  pollDatasetsForLocks(): void {
    /**
     * Polls dataset locks for dataset ids in the datasetsToPollLocks list.
     */
    let modify = false;
    let subscription = this.apiService.retrieveAllLocks().subscribe(
      (currentLocks) => {
        for (let datasetId of this.datasetsToPollLocks) {
          let currentLocksDataset = new Set(currentLocks[datasetId]);
          let previousLocksDataset = new Set(this.datasetLocks.value[datasetId]);
          if (currentLocksDataset.size === previousLocksDataset.size && [...currentLocksDataset].every(value => previousLocksDataset.has(value))) {
          } else {
            modify = true;
            this.datasetsToPollLocks.delete(datasetId)
          };
        };
        if (modify) {
          this.clearDatasets();
          this.updateDatasets();
        }
      });
  }

  updateDatasetsToPollLocksLists(): void {
    /**
     * Updates the datasetsToPollLocks list according to the locks set in Dataverse.
     */
    let subscription = this.apiService.retrieveAllLocks().subscribe(
      (allLocks) => {
        this.datasetLocks.next(allLocks);
        for (let datasetId of Object.keys(allLocks)) {
          if (allLocks[datasetId].includes('publishing') || allLocks[datasetId].includes('finalizePublication')) {
            this.datasetsToPollLocks.add(datasetId);
          }
        }
        subscription.unsubscribe();
      });
  }

  clearDatasets(): void {
    /**
     * Clears the datasets$ observable.
     */
    this.datasets$ = of([]);
  }

  updateDatasets(): void {
    /** 
     * Updates the currently cached and displayed dataset information.
     * */
    this.modified.next(Date());
  }




  assignReviewerToDataset(datasetId: string, reviewer: string): Subscription {
    /**
     * Assigns a reviewer to a dataset.
     */
    let result = this.apiService.assignReviewer(datasetId, reviewer).subscribe(
      {
        next: (response) => {
          this.clearDatasets();
          this.updateDatasets();

        }
      }
    );
    return result;

  }


  unAssignReviewerFromDataset(datasetId: string): Subscription {
    /**
     * Unassigns a reviewer to a dataset.
     */

    let result = this.apiService.unAssignReviewer(datasetId).subscribe(
      {
        next: (response) => {
          this.clearDatasets();
          this.updateDatasets();
        }
      }
    );

    return result;
  }

  getDepartmentTags(dataset: Dataset | null): NoteTag[] {
    /** 
     * Returns the tags containing department information of the dataset. 
     * */
    let result: NoteTag[] = [];
    for (let department of dataset?.department || []) {
      result.push({ type: 'department', 'content': department })
    }
    return result;
  }

  getFacultyTags(dataset: Dataset | null): NoteTag[] {
    /** 
     * Returns the tags containing faculty information of the dataset. 
     * */

    let result: NoteTag[] = [];
    for (let faculty of dataset?.faculty || []) {
      result.push({ type: 'faculty', 'content': faculty })
    }
    return result;
  }

  getStatusText(dataset: Dataset | null): string {
    /** 
     * Returns the status of of the dataset as text.
     */
    if (!dataset) { return 'N/A' }
    switch (dataset.status) {
      case Dataset.Status.InReview: return 'In review';
      case Dataset.Status.SubmittedForReview: return 'Submitted for review';
      case Dataset.Status.Returned: return 'Returned to author';
      case Dataset.Status.Draft: return 'Draft';
      case Dataset.Status.Deaccessioned: return 'Deaccessioned';
      case Dataset.Status.Published: return 'Published';
    }
    return dataset.status;


  }

  getLockTags(dataset: Dataset | null): NoteTag[] {
    /**
     * Returns the locks of the dataset as tags.
     */
    let result: NoteTag[] = [];
    let lockLablesMap = new Map<string, string>([
      ['publishing', 'Publishing...'],
      ['finalizePublication', 'Publishing...'],
    ]);
    for (let lock of lockLablesMap.keys()) {
      if ((dataset?.locks || []).includes(lock)) {
        result.push({ type: 'lock', content: lockLablesMap.get(lock) || '' });
      }
    }
    return result;
  }

  getSuppostRequestTags(datasetId: string | null): Observable<NoteTag[]> {
    /** 
     * Returns the support request status of the dataset as tag. 
     */
    let result: Observable<NoteTag[]> = of([])
    if (datasetId) {
      result = this.apiService.retrieveSupportRequest(datasetId);
    }
    return result;
  }

  getDepartmentAndFacultyTags(dataset: Dataset): NoteTag[] {
    /** 
     * Returns department and faculty tags of a dataset.  
     */
    let tags: NoteTag[] = [];
    tags = tags.concat(this.getDepartmentTags(dataset));
    tags = tags.concat(this.getFacultyTags(dataset));
    return tags;
  }

  getTags(dataset: Dataset | null): NoteTag[] {

    let tags: NoteTag[] = [];
    if (dataset) {
      tags = tags.concat(this.getLockTags(dataset));
      tags.push(this.getStatusTag(dataset));
    }
    return tags;
  }

  getStatusTag(dataset: Dataset): NoteTag {
    /** 
   * Returns the status of a dataset as tags.
   */

    return { type: 'status', content: this.getStatusText(dataset) }
  }
  getTagsAsObservable(dataset: Dataset): Observable<NoteTag[]> {
    /** 
    * Returns tags of a dataset.  
    */

    if (dataset) {
      return this.apiService.retrieveReviewTags(dataset.identifier).pipe(
        map(
          (tags) => {

            return tags
          }))
    } else { return of([]) }
  }
  getReviewerTags(dataset: Dataset | null): Observable<NoteTag[]> {
    /** 
   * Returns tags of a dataset as observable.  
   */
    return this.userService.getUserInfo(dataset?.reviewer.at(0) || null)
      .pipe(
        map(
          (reviewer) => {
            let result: NoteTag[] = [];
            if (reviewer) {
              result.push({ type: 'reviewer', content: reviewer.userfirstname || '' });

            }
            if (result.length == 0 && dataset?.status == Dataset.Status.SubmittedForReview) {
              result.push({ type: 'reviewer', content: 'Unassigned' });
            }
            return result;
          }
        )
      )
  }
}
