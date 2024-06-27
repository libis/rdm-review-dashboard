import { Injectable } from '@angular/core';
import { Observable, of } from "rxjs";
import { Dataset, DatasetCount, DatasetContact } from "../models/dataset";
import { HttpClient } from '@angular/common/http';
import { User } from '../models/user.model';
import { AppConfigService } from './app-config.service';
import { Note, NoteTag } from '../models/note.model';
@Injectable({
  providedIn: 'root'
})
export class ApiService {
  /* Service for calls to Review Dashboard API
   * that retrieve data from the API start with retrieve 
   */
  baseUrl!: string;
  constructor(
    private http: HttpClient,
    private config: AppConfigService) {
    this.baseUrl = this.config.apiUrl;

  }



  retrieveCurrentUsername(): Observable<any> {
    /* 
     * Retrieves from the Review Dashboard API the username of the currently logged user.
     */
    return this.http.get<any>(`${this.baseUrl}/users/:me`, { observe: 'response' });
  }

  retrieveCurrentUserDetails() {
    /* Retrieves from the Review Dashboard API details of the currently logged user.*/
    return this.http.get<User>(`${this.baseUrl}/users/:me`);

  }


  retrieveDatasets(start: number | null, rows: number | null, status: string | null, reviewer: string | null): Observable<Dataset[]> {
    /*
     * Retrieves from the Review Dashboard API datasets with their relevant metadata.  
     */

    let params: string[] = [];

    if (start) {
      params.push(`start=${start}`)
    }
    if (rows) {
      params.push(`rows=${rows}`)
    }
    if (status) {
      params.push(`status=${status}`)
    }
    if (reviewer) {
      params.push(`reviewer=${reviewer}`)
    }

    let url = `${this.baseUrl}/datasets`
    if (params.length > 0) {
      url = url + '?' + params.join('&')
    }


    return this.http.get<Dataset[]>(url);
  }


  retrieveDatasetDetails(datasetId: string): Observable<Dataset> {
    /*
     * Retrieves from the Review Dashboard API the details of a dataset with its relevant metadata.  
     */
    return this.http.get<Dataset>(`${this.baseUrl}/datasets/${datasetId}`);
  }

  retrieveAvailableReviewers(): Observable<User[]> {
    /*
     * Retrieves from the Review Dashboard API a list of users that have right to review datasets. 
     * The roles that can review are defined in the backend configuration.
     */

    return this.http.get<User[]>(`${this.baseUrl}/reviewers`);
  }

  retrieveUserDetails(userId: string | null): Observable<User | null> {
    if (userId) {
      return this.http.get<User>(`${this.baseUrl}/users${userId}`);
    } else {
      return of(null);
    }
  }

  retrieveDatasetStatusCount(reviewer: string | null) {
    if (reviewer != null) {
      return this.http.get<DatasetCount[]>(`${this.baseUrl}/datasets/stats/reviewStatus?reviewer=${reviewer}`);
    } else {
      return this.http.get<DatasetCount[]>(`${this.baseUrl}/datasets/stats/reviewStatus`);
    }

  }

  retrieveDatasetIssues(datasetId: string | null): Observable<any> {
    /*
     * Retrieves from the Review Dashboard API the list of issues and warnings that the dataset has. 
     * 
     */
    if (datasetId) {
      return this.http.get<any[]>(`${this.baseUrl}/datasets/${datasetId}/issues`);
    } else {
      return of([])
    }
  }

  updateDatasetIssuesChecklist(datasetId: string, checklist: string[]) {
    /* 
     * Updates the issues checklist for the dataset using the Review Dashboard API. 
     */
    let url = `${this.baseUrl}/datasets/${datasetId}/issues/checklist`;
    let body = { issues: checklist }
    return this.http.post(url, body).subscribe();
  }


  assignReviewer(datasetId: string, reviewer: string) {
    /*
     * Assigns as reviewer the user with the given user to the dataset with the id, using the Review Dashboard API.
     * 
     */

    let url = `${this.baseUrl}/datasets/${datasetId}/reviewer/:replace?reviewer=${reviewer}`;


    return this.http.post(url, null);

  }
  unAssignReviewer(datasetId: string) {
    /*
     * Removes all the reviewers from dataset with the id, using the Review Dashboard API.
     */
    let url = ''
    url = `${this.baseUrl}/datasets/${datasetId}/reviewer`;

    return this.http.delete(url);

  }

  publishDataset(datasetId: string, version: string | null) {
    /* Publishes the given dataset */
    let url = `${this.baseUrl}/datasets/${datasetId}/:publish?version=${version}`;
    let body = {}
    return this.http.post(url, body, { responseType: 'json' });

  }

  returnDataset(datasetId: string, reason: string | null) {
    /* Returns the given dataset to author, with optional reason for return*/
    let url = `${this.baseUrl}/datasets/${datasetId}/:return`;
    let body = { reason: reason }

    return this.http.post(url, body, { responseType: 'json' });

  }

  updateFeedback(datasetId: string, feedback: string | null) {
    /* Updates the feedback text for the dataset. 
     * The Feedback text is the text that will be emailed to the author when it is returned to the author. 
     * Only the latest feedback text is saved, therefore this call will replace the previous feedback.  
     */
    let url = `${this.baseUrl}/datasets/${datasetId}/feedback`;
    let body = { text: feedback }
    return this.http.post(url, body);
  }

  retrieveFeedback(datasetId: string) {
    /* 
     * Retrieves from the Review Dashboard API the feedback text for the dataset.  */
    let url = `${this.baseUrl}/datasets/${datasetId}/feedback`;
    return this.http.get<Note>(url);
  }

  retrieveAutoGeneratedFeedback(datasetId: string) {
    /* 
     * Autogenerates feedback email using the Review Dashboard API for the dataset, and returns it.  
    */
    let url = `${this.baseUrl}/datasets/${datasetId}/feedback/:generate`;
    return this.http.get<Note>(url);
  }

  updateInternalNote(datasetId: string, note: string) {
    /* Updates the feedback text for the dataset. 
     * The Feedback text is the text that will be emailed to the author when it is returned to the author. 
     * Only the latest feedback text is saved, therefore this call will replace the previous feedback.  
     */
    let url = `${this.baseUrl}/datasets/${datasetId}/internal_note`;
    let body = { text: note }
    return this.http.post(url, body);
  }


  retrieveInternalNote(datasetId: string) {
    /** Returns the internal review note for the dataset.  */
    let url = `${this.baseUrl}/datasets/${datasetId}/internal_note`;
    return this.http.get<Note>(url);
  }


  retrieveHistory(datasetId: string) {
    /* Retrieves the (automatically generated) review history of the dataset. 
    */
    let url = `${this.baseUrl}/datasets/${datasetId}/history`;
    return this.http.get<Note[]>(url);
  }

  setReviewTags(datasetId: string, tags: NoteTag[]) {
    /* 
    * Updates the custom review tags for the dataset using the Review Dashboard API. 
    * Currently used for the 'Support Requested' tag. 
    */
    let url = `${this.baseUrl}/datasets/${datasetId}/review_tags`;
    let body = { tags: tags }
    return this.http.post(url, body);

  }

  retrieveReviewTags(datasetId: string) {
    /* 
    * Updates the custom review tags for the dataset using the Review Dashboard API. 
    */

    let url = `${this.baseUrl}/datasets/${datasetId}/review_tags`;
    return this.http.get<NoteTag[]>(url);

  }

  retrieveLocks(datasetId: string) {
    /* 
    * Retrieves from the Review Dashboard API the locks for a dataset. 
    * This is used to display 'publishing' tag. 
    */
    let url = `${this.baseUrl}/datasets/${datasetId}/locks`;
    return this.http.get<string[]>(url);
  }


  retrieveAllLocks() {
    /* 
    * Retrieves from the Review Dashboard API locks for all the datasets. 
    * This is used to display 'publishing' tag. 
    */

    let url = `${this.baseUrl}/locks`;
    return this.http.get<any>(url);
  }

  askSupport(datasetId: string) {
    /*
     * Adds the 'Support requested' tag to a dataset, using the Review Dashboard API. 
     */
    let url = `${this.baseUrl}/datasets/${datasetId}/support_request`;
    let body = {}
    return this.http.post<NoteTag[]>(url, body);
  }

  removeSupportRequest(datasetId: string) {
    /**\
    * Removes the 'Support requested' tag from a dataset, using the Review Dashboard API. 
    */

    let url = `${this.baseUrl}/datasets/${datasetId}/support_request`;
    let body = {}
    return this.http.delete<NoteTag[]>(url, body);

  }

  retrieveSupportRequest(datasetId: string) {
    /*
    * Retrieves the 'Support requested' tag of a dataset, using the Review Dashboard API. 
    */

    let url = `${this.baseUrl}/datasets/${datasetId}/support_request`
    return this.http.get<NoteTag[]>(url);
  }

  retrieveDatasetContributor(datasetId: string) {
    /*
    * Retrieves the contributor information for a dataset, using the Review Dashboard API. 
    */
    let url = `${this.baseUrl}/datasets/${datasetId}/assignees/contributor`
    return this.http.get<User[]>(url);
  }

  retrieveDatasetContact(datasetId: string) {
    /*
    * Retrieves the contact information for a dataset, using the Review Dashboard API. 
    */
    let url = `${this.baseUrl}/datasets/${datasetId}/contact`
    return this.http.get<DatasetContact[]>(url);
  }

} 