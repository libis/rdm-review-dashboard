import { Injectable } from '@angular/core';
import { User } from '../models/user.model'
import { of, BehaviorSubject, Observable, map, combineLatest } from 'rxjs';
import { ApiService } from './api.service';
import { Router } from '@angular/router';
import { ActivatedRoute } from '@angular/router';
@Injectable({
  providedIn: 'root'
})
export class UserService {

  loggedUserId: BehaviorSubject<string | null> = new BehaviorSubject<string | null>(null);
  reviewers: BehaviorSubject<User[]> = new BehaviorSubject<User[]>([]);
  loggedUserDetails$: Observable<User | null> = of(null);
  reviewers$!: Observable<User[]>;




  assignableReviewers: BehaviorSubject<User[]> = new BehaviorSubject<User[]>([]);
  isAuthorizedToReview$: Observable<boolean>;
  loggedUserDetails: BehaviorSubject<User | null> = new BehaviorSubject<User | null>(null);


  constructor(private apiService: ApiService, private router: Router, private route: ActivatedRoute) {


    this.reviewers$ = apiService.retrieveAvailableReviewers();
    this.loggedUserDetails$ =
      combineLatest([
        this.loggedUserId.asObservable(),
        this.reviewers$
      ]).pipe(
        map(
          ([userId, reviewers]) => {
            let userDetails = reviewers.find(
              (reviewer) =>
                this.removeAtChar(reviewer.username) == this.removeAtChar(userId) || null);
            this.loggedUserDetails.next(userDetails || null);
            return userDetails || null;
          }
        )
      )

    this.isAuthorizedToReview$ = this.loggedUserDetails$.pipe(
      map(
        user => user?.isAdmin || user?.isReviewer || false
      )
    )

    this.apiService.retrieveAvailableReviewers().subscribe(
      {
        next: (reviewerList) => {
          this.reviewers.next(reviewerList);
        },
        error: (err: any) => {
          this.reviewers.error(err);
        },
        complete: () => {
          this.reviewers.complete();
        }
      }
    );
  }



  removeAtChar(s: string | null): string | null {
    /** 
     * Removes the '@' at the beginning of the string.
     */
    let result = s
    if (s && s.startsWith('@')) {
      result = s.slice(1);


    }
    return result;
  }

  getUserInfo(userId: string | null): Observable<User | null> {
    /** 
     * Gets name and relevant information for the user with the given id, from the list of reviewers.
     */
    return this.reviewers$
      .pipe(
        map(
          reviewers => {
            return reviewers.find(
              (reviewer) => this.removeAtChar(reviewer.username) == this.removeAtChar(userId)
            ) || null;
          }
        )
      )
  }
}
