import { Component, OnInit } from '@angular/core';
import { ApiService } from "../services/api.service";
import { DatasetService } from "../services/dataset.service";
import { BehaviorSubject, map, Observable, of, switchMap, combineLatest, shareReplay } from "rxjs";
import { Dataset } from "../models/dataset";
import { debounceTime, distinctUntilChanged } from 'rxjs/operators';
import { PaginatorState } from 'primeng/paginator';
import { UserService } from '../services/user.service';

@Component({
  selector: 'app-selection-list',
  templateUrl: './selection-list.component.html',
  styleUrls: ['./selection-list.component.scss']
})
export class SelectionListComponent implements OnInit {

  datasets$!: Observable<Dataset[]>;
  datasetTabs!: Map<string, Observable<Dataset[]>>;
  tabIndex: number = 0
  selectedTab: BehaviorSubject<number> = new BehaviorSubject(this.tabIndex);
  firstRecord: BehaviorSubject<number> = new BehaviorSubject(0);
  rows: BehaviorSubject<number> = new BehaviorSubject<number>(9);
  itemsPerPage: number = 9;
  datasetCount$!: Observable<number>;

  constructor(public apiService: ApiService,
    public datasetService: DatasetService,
    public userService: UserService
  ) {
    this.datasetService.updateDatasets();

    this.datasets$ = combineLatest([
      this.datasetService.modified.asObservable(),
      this.selectedTab.asObservable(),
      this.firstRecord.asObservable(),
      this.rows.asObservable().pipe(
        debounceTime(1000),
        distinctUntilChanged()
      )

    ]).pipe(
      switchMap(
        ([modified, selectedTab, firstRecord, rows]) => {
          switch (selectedTab) {

            case 0:
              {
                return apiService.retrieveDatasets(firstRecord, rows, 'in_review', this.userService.loggedUserId.value);
              }
            case 1: {
              return apiService.retrieveDatasets(firstRecord, rows, 'submitted_for_review', null);
            }
            case 2:
              {
                return apiService.retrieveDatasets(firstRecord, rows, 'in_review', null);
              }
            case 3: {
              return apiService.retrieveDatasets(firstRecord, rows, 'published', null);
            }
            case 4: {
              return apiService.retrieveDatasets(firstRecord, rows, 'draft', null);
            }
            case 5: {
              return apiService.retrieveDatasets(firstRecord, rows, null, null);
            }
            default:
              return of([]);
          }

        }
      )
    )

    this.datasetCount$ = combineLatest([
      this.datasetService.modified.asObservable(),
      this.selectedTab.asObservable(),
      this.datasetService.datasetCount$,
      this.datasetService.loggedUserDatasetCount$]).pipe(
        map(
          ([modified, selectedTab, datasetCount, loggedUserDatasetCount]) => {
            switch (selectedTab) {

              case 0:
                {
                  return loggedUserDatasetCount.find(c => c.status == 'in_review')?.count || 0;
                }
              case 1: {
                return datasetCount.find(c => c.status == 'submitted_for_review')?.count || 0;
              }
              case 2:
                {
                  return datasetCount.find(c => c.status == 'in_review')?.count || 0;
                }
              case 3: {
                return datasetCount.find(c => c.status == 'published')?.count || 0;
              }
              case 4: {
                return datasetCount.find(c => c.status == 'draft')?.count || 0;
              }
              case 5: {
                return datasetCount.find(c => c.status == 'all')?.count || 0;
              }
              default:
                return 0;
            }
          }


        ),
        shareReplay(1)
      )
  }



  ngOnInit(): void {

  }

  onPageChange(event: PaginatorState) {
    this.firstRecord.next(event.first ?? 0);
    this.rows.next(event.rows ?? 9);
  }
  isInt(value: any) {
    return !isNaN(value) &&
      parseInt(value) == value &&
      !isNaN(parseInt(value, 10));
  }

  onNumberOfItemsChange() {
    if (this.itemsPerPage != this.rows.value) {
      this.rows.next(this.itemsPerPage)
    }

  }
  onTabChange(event: any) {
    this.firstRecord.next(0);
    this.selectedTab.next(event.index);
  }

}

