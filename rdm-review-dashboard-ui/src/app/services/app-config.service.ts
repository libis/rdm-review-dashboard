import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';


@Injectable({
  providedIn: 'root'
})
export class AppConfigService {
  private config: any;
  constructor(private http: HttpClient, private router: Router) {
  }

  loadConfig() {
    return this.http.get('assets/settings.json')
      .toPromise()
      .then(data => {
        this.config = data;
      }
      );
  }

  get apiUrl() {
    let apiUrl = this.config.apiUrl + '/api';
    return apiUrl;
  }

  get dataverseUrl() {
    let dataverseUrl = this.config.dataverseUrl;
    return dataverseUrl;
  }

  get dataverseName() {
    let dataverseName = this.config.dataverseName;
    return dataverseName;
  }
}



