import { Component, Signal, OnDestroy } from '@angular/core';
import { ApiService } from '../../services/api-service';
import { Observable, map, of, catchError, throwError } from 'rxjs';
import { ButtonModule } from 'primeng/button';
import { SelectModule } from 'primeng/select';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { ProgressSpinnerModule } from 'primeng/progressspinner';
import { DatasetService } from '../../services/dataset.service';
import { CardModule } from 'primeng/card';
import { toSignal } from '@angular/core/rxjs-interop';
import { DividerModule } from 'primeng/divider';
import { AccordionModule } from 'primeng/accordion';
import { Config } from '../../services/config';

interface DatasetOption {
  identifier: string;
  title: string;
  optionLabel: string;
}

interface OrhcestratorTaskStatus {
  id: string;
  task_id: string;
  started: string;
  finished: string | null;
  subtasks: string[];
  results: any[];
  status: string;
}

@Component({
  selector: 'app-dataset-selection',
  imports: [
    AccordionModule,
    ButtonModule,
    CardModule,
    DividerModule,
    SelectModule,
    FormsModule,
    ProgressSpinnerModule,
  ],
  templateUrl: './dataset-selection.html',
  styleUrl: './dataset-selection.scss',
})
export class DatasetSelection implements OnDestroy {
  datasetList$: Observable<DatasetOption[] | null> = of(null);
  datasetOptionsList: Signal<DatasetOption[] | undefined>;
  selectedDataset: DatasetOption | undefined;
  helpDeskEmail: string;
  dataverseName: string;
  introHTML: string;
  supportLink: string;
  constructor(
    private api: ApiService,
    private router: Router,
    private route: ActivatedRoute,
    private datasetService: DatasetService,
    private config: Config,
  ) {
    this.datasetService.setMetadata(null);
    this.datasetOptionsList = toSignal(
      this.api.retrieveDatasetsForUser('userId').pipe(
        map((datasetArray) =>
          datasetArray.map((dataset) => ({
            identifier: dataset.identifier,
            title: dataset.title,
            optionLabel: dataset.identifier + ' - ' + dataset.title,
          })),
        ),
        catchError((error) => {
          if (error.status === 404) {
            console.error('User datasets not found');
            return of([]); 
          } else if (error.status >= 500) {
            console.error('Server error:', error);
            return of([]);
          }
          return throwError(() => error);
        }),
      ),
    );
    this.helpDeskEmail = this.config.helpDeskEmail;
    this.dataverseName = this.config.dataverseName;
    this.introHTML = this.config.introHTML;
    this.supportLink = this.config.supportLink
  }

  getIntroHTML() {
    let result = this.introHTML;
    result = result.replaceAll("{helpDeskEmail}", this.helpDeskEmail);
    result = result.replaceAll("{dataverseName}", this.dataverseName);
    result = result.replaceAll("{supportLink}", this.supportLink);
    return result;
  }

  onClickNext() {
    if (this.selectedDataset?.identifier) {
      this.api.startChecks(this.selectedDataset.identifier).subscribe((response) => {
        if ((response as OrhcestratorTaskStatus)?.status === 'running') {
          this.router.navigate(['checklist', this.selectedDataset?.identifier]);
        } else {
          console.log('response: ', response);
        }
      });
    }
  }

  ngOnDestroy() {}
}
