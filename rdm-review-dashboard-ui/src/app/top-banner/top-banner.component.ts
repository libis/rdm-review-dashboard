import { Component, OnInit } from '@angular/core';
import { UserService } from '../services/user.service';
import { Router } from '@angular/router';
import { Observable, map } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { User } from '../models/user.model';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
@Component({
  selector: 'app-top-banner',
  templateUrl: './top-banner.component.html',
  styleUrls: ['./top-banner.component.scss'],
  providers: []

})
export class TopBannerComponent implements OnInit {
  display: boolean = false;
  user: Observable<User | null>;
  customHeader!: SafeHtml;
  constructor(public userService: UserService, private http: HttpClient, private router: Router, private sanitizer: DomSanitizer) {
    this.user = this.userService.loggedUserDetails$;
  }
  ngOnInit() {
    this.http.get('assets/header.html', { responseType: 'text' })
      .pipe(map((headerHTML) => this.sanitizer.bypassSecurityTrustHtml(headerHTML)))
      .subscribe((sanitizedHTML) => {
        this.customHeader = sanitizedHTML;
      });
  }

}

