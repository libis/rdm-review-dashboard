import { Component, OnDestroy } from '@angular/core';
import { ReviewService } from '../services/review.service';
import { Router, Event, NavigationStart, NavigationEnd, NavigationError, ActivatedRoute } from '@angular/router';
import { Subscription, BehaviorSubject } from 'rxjs';

interface ReviewState {
  enabled: boolean,
  active: boolean
}

@Component({
  selector: 'div[app-progress-section]',
  templateUrl: './progress-section.component.html',
  styleUrls: ['./progress-section.component.scss']
})
export class ProgressSectionComponent implements OnDestroy {

  unlocked = {
    active: false,
    enabled: true
  }

  active = {
    active: true,
    enabled: true
  }

  locked = {
    active: false,
    enabled: false
  }

  currentState!: string;
  select: BehaviorSubject<ReviewState> = new BehaviorSubject<ReviewState>(this.locked);
  detail: BehaviorSubject<ReviewState> = new BehaviorSubject<ReviewState>(this.locked);
  feedback: BehaviorSubject<ReviewState> = new BehaviorSubject<ReviewState>(this.locked);
  publish: BehaviorSubject<ReviewState> = new BehaviorSubject<ReviewState>(this.locked);
  subscription!: Subscription;



  constructor(private reviewService: ReviewService, private router: Router, private route: ActivatedRoute) {

    this.currentState = this.getStateFromUrl(this.router.url);
    this.setState(this.currentState);
    this.subscription = this.router.events.subscribe((event: Event) => {
      if (event instanceof NavigationStart) {
      }

      if (event instanceof NavigationEnd) {
        let state = this.getStateFromUrl(event.url);
        this.setState(state);
      }

      if (event instanceof NavigationError) {

      }
    });
  }
  ngOnDestroy() {
    this.subscription.unsubscribe();
  }


  getStateFromUrl(url: string) {
    let state = 'datasets';
    for (let s of ['select', 'feedback', 'publish']) {
      if (url.includes(s)) {
        state = s;
      }
    }
    return state;

  }

  selectionChanged() {

  }

  setState(newState: string) {


    if (newState == 'select') {
      this.select.next(this.active);
      this.detail.next(this.locked);
      this.feedback.next(this.locked);
      this.publish.next(this.locked);

    }
    else if (newState == 'datasets') {
      this.select.next(this.unlocked);
      this.detail.next(this.active);
      this.feedback.next(this.locked);
      this.publish.next(this.locked);

    } else if (newState == 'feedback') {
      this.select.next(this.unlocked);
      this.detail.next(this.unlocked);
      this.feedback.next(this.active);
      this.publish.next(this.locked);  

    } else if (newState == 'publish') {
      this.select.next(this.unlocked);
      this.detail.next(this.unlocked);
      this.feedback.next(this.unlocked);
      this.publish.next(this.active);
    }


    this.currentState = newState
  }

  onClickSelect() {

    this.reviewService.selectedDatasetId.next(null);
    this.router.navigate(['select']).then();

  }
  onClickDetail() {
    if (this.reviewService.selectedDatasetId.value) {
      this.router.navigate(['datasets', this.reviewService.selectedDatasetId.value]).then();
    }
  }
  onClickReview() {
    if (this.reviewService.selectedDatasetId.value && this.reviewService.canLoggedUserReadSelectedDataset()) {
      this.router.navigate(['feedback', this.reviewService.selectedDatasetId.value]).then();
    }
  }
  onClickPublish() {
    if (this.reviewService.selectedDatasetId.value && this.reviewService.canLoggedUserReadSelectedDataset()) {
      this.router.navigate(['publish', this.reviewService.selectedDatasetId.value]).then();
    }
  }

}
