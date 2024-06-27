import { Component, OnDestroy } from '@angular/core';
import { ReviewService } from '../services/review.service';
import { Router, Event, NavigationStart, NavigationEnd, NavigationError, ActivatedRoute } from '@angular/router';
import { Subscription } from 'rxjs';

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

  currentState!: string;
  select!: ReviewState;
  detail!: ReviewState;
  feedback!: ReviewState;
  publish!: ReviewState;
  subscription!: Subscription;
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



  constructor(private reviewService: ReviewService, private router: Router, private route: ActivatedRoute) {

    this.currentState = 'select';

    this.setState('select');
    this.subscription = this.router.events.subscribe((event: Event) => {
      if (event instanceof NavigationStart) {
      }

      if (event instanceof NavigationEnd) {
        let url = event.url;
        let state = 'datasets';
        for (let s of ['select', 'feedback', 'publish']) {
          if (url.includes(s)) {
            state = s;
          }
        }
        this.setState(state);
      }

      if (event instanceof NavigationError) {

      }
    });
  }
  ngOnDestroy() {
    this.subscription.unsubscribe();
  }

  selectionChanged() {

  }

  setState(newState: string) {


    if (newState == 'select') {
      this.select = this.active;
      this.detail = this.locked;
      this.feedback = this.locked;
      this.publish = this.locked;

    }
    else if (newState == 'datasets') {
      this.select = this.unlocked;
      this.detail = this.active;
      this.feedback = this.locked;
      this.publish = this.locked;

    } else if (newState == 'feedback') {
      this.select = this.unlocked;
      this.detail = this.unlocked;
      this.feedback = this.active;
      this.publish = this.locked;

    } else if (newState == 'publish') {
      this.select = this.unlocked;
      this.detail = this.unlocked;
      this.feedback = this.unlocked;
      this.publish = this.active;
    }
    if (!this.reviewService.canLoggedUserReadSelectedDataset())
      this.feedback = this.locked;
    this.publish = this.locked;


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
