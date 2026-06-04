import { Injectable, signal, WritableSignal } from '@angular/core';
import { Dataset, DatasetBasicMetadata } from '../models/dataset';
import { ApiService } from './api-service';
import { ActivatedRoute, Router } from '@angular/router';
import { Observable, of, map } from 'rxjs';
import { toSignal } from '@angular/core/rxjs-interop';
import { Config } from './config';

@Injectable({
  providedIn: 'root',
})
export class DatasetService {
  datasetBasicMetadata: DatasetBasicMetadata | null = null;
  dataset: WritableSignal<Dataset | null> = signal(null);
  datasetId?: WritableSignal<string | null>;
  dataset$: Observable<Dataset | null> = of(null);
  constructor(private api: ApiService) {}

  setMetadata(dataset: DatasetBasicMetadata | null) {
    this.datasetBasicMetadata = dataset;
    console.log(this.datasetBasicMetadata);
  }

  retrieve(datasetId: string) {
    console.log('this runs');
    if (datasetId !== null && datasetId !== this.dataset()?.identifier) {
      console.log(`retrieving dataset with Id ${datasetId}`);
      this.api.retrieveDataset(datasetId).subscribe((dataset) => this.dataset.set(dataset));
    }
  }

  getDatasetUrl() {
    return this.dataset()?.datasetUrl;
  }
}
