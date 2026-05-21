import { Injectable } from '@angular/core';
import { Config } from './config';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Dataset } from '../models/dataset';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  constructor(
    private config: Config,
    private http: HttpClient,
  ) {}

  delay(ms: number) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  startChecks(datasetId: string) {
    let url = `${this.config.apiUrl}/datasets/${datasetId}/:startChecks`;
    let body = null;
    console.log('running checks for ', datasetId);
    return this.http.post(url, body);
  }

  pollResults(datasetId: string) {
    let url = `${this.config.apiUrl}/datasets/${datasetId}/:pollResults`;
    return this.http.get(url);
  }

  retrieveDatasetsForUser(userId: string): Observable<Dataset[]> {
    let url = `${this.config.apiUrl}/users/:me/assignedDatasets`;
    return this.http.get<Dataset[]>(url);
  }

  retrieveDataset(datasetId: string): Observable<Dataset> {
    let url = `${this.config.apiUrl}/datasets/${datasetId}`;
    return this.http.get<Dataset>(url);
  }

}
