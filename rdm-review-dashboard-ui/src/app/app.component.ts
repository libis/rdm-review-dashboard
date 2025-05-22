import { Component, OnInit } from '@angular/core';
import { UserService } from './services/user.service';
import { Router, ActivatedRoute } from '@angular/router';
import { ApiService } from './services/api.service';
import { HttpResponse } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { HttpClient } from '@angular/common/http';
import { map } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  customFooter!: SafeHtml;

  constructor(
    public user: UserService,
    private apiservice: ApiService,
    private router: Router,
    private route: ActivatedRoute,
    private http: HttpClient,
    private sanitizer: DomSanitizer) {
    let uid_header = null;
    let uid_response = null;
    this.apiservice.retrieveCurrentUsername().subscribe(
      (data: HttpResponse<any>) => {

        uid_header = data.headers.get('x-user');
        uid_response = data.body.id;
        uid_header = user.removeAtChar(uid_header);
        if (environment.production) {
          this.user.loggedUserId.next(uid_header);
        } else {
          this.user.loggedUserId.next(uid_response);
        }
        if (!this.user.loggedUserId.value) {
          router.navigate(['/']).then();
        }    
      }
    );

  }
  ngOnInit() {
    this.http.get('assets/footer.html', { responseType: 'text' })
      .pipe(map((footerHTML) => this.sanitizer.bypassSecurityTrustHtml(footerHTML)))
      .subscribe((sanitizedHTML) => {
        this.customFooter = sanitizedHTML;
      });
  }

}
