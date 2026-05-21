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
}
