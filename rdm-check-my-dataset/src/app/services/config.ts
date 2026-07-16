import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
@Injectable({
  providedIn: 'root',
})
export class Config {
  constructor(private http: HttpClient) {}
  private config: any;

  loadConfig() {
    return this.http
      .get('assets/settings.json')
      .toPromise()
      .then((data) => {
        this.config = data;
      });
  }
  get apiUrl() {
    let apiUrl = this.config.apiUrl + '/api';
    return apiUrl;
  }

  get helpDeskEmail() {
    return this.config.helpDeskEmail;
  }
  get dataverseName() {
    return this.config.dataverseName;
  }
  get supportLink() {
    return this.config.supportLink;
  }
  get introHTML() {
    return this.config.introHTML;
  }
  get allChecksSucceededHTML() {
    return this.config.allChecksSucceededHTML;
  }
  get noResultWarning() {
    console.log('noResultWarning', this.config.noResultWarning);
    return this.config.noResultWarning;
  }

}
