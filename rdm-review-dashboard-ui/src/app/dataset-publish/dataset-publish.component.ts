import { Component, OnInit } from '@angular/core';
import { ReviewService } from '../services/review.service';
import { Router } from '@angular/router';
import { UserService } from '../services/user.service';

interface PublishOption {
  label: string,
  value: string
}
@Component({
  selector: 'app-publish',
  templateUrl: './dataset-publish.component.html',
  styleUrls: ['./dataset-publish.component.scss']
})
export class DatasetPublishComponent implements OnInit {
  versionOptions!: PublishOption[];
  selectedVersionType: string = "major";
  firstPublish!: boolean;
  publishDialogContent: string = '';
  feedbackTextAsHTML!: string;
  locked: boolean;

  constructor(
    public reviewService: ReviewService,
    public userService: UserService,
    private router: Router
  ) {

    this.feedbackTextAsHTML = this.reviewService.selectedDatasetSavedFeedback.value?.replace(/(?:\r\n|\r|\n)/g, '<br>') || '';
    this.locked = this.reviewService.isLockedForReviewing()
    console.log(this.reviewService.selectedDatasetToBePublished);
  }

  ngOnInit(): void {

    if (this.reviewService.selectedDatasetToBePublished == null) {
      this.router.navigate(['/feedback', this.reviewService.selectedDatasetId.value]).then();
    }
    this.versionOptions = [];
    if (!this.reviewService.selectedDataset.value?.version) {
      this.firstPublish = true;
    } else {

      this.firstPublish = false;
      this.versionOptions.push({ label: `Major (${(Math.trunc(this.reviewService.selectedDataset.value.version || 0) + 1).toFixed(1)}) `, value: "major" })
      this.versionOptions.push({ label: `Minor (${((this.reviewService.selectedDataset.value.version || 0) + .1).toFixed(1)}) `, value: "minor" })
      this.versionOptions.push({ label: `Update current version (${(this.reviewService.selectedDataset.value.version || 0).toFixed(1)}) `, value: "updateCurrent" })
    }
  }
  delay(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  publish() {

    let version = this.reviewService.selectedDataset.value?.version || 0;
    if (version) {
      if (this.selectedVersionType == 'major') {
        version = Math.trunc(version) + 1;
      } else if (this.selectedVersionType == 'minor') {
        version = version + .1;
      }
    } else {
      version = 0
    }
    this.reviewService.clearDatasets();
    let publishSubscription = this.reviewService.publishSelected(this.selectedVersionType || 'major').subscribe(
      {
        next: (publishResult) => {
          const publishResultContent = publishResult.toString();
          if (!publishResultContent.includes('ERROR')) {
            this.reviewService.unAssignReviewer();
            if (this.selectedVersionType == 'updateCurrent') {
              window.alert(`The dataset is being published as the current version (${version.toFixed(1)}...`);
            } else if (version != 0) {
              window.alert(`The dataset is being published as a ${this.selectedVersionType} version (${version.toFixed(1)})...`);
            } else {
              window.alert(`The dataset is being published as the 1.0 version...`);
            }

          } else if (publishResultContent.includes('Re-try as major release') || publishResultContent.includes('Dataset Version Update failed.')) {
            window.alert(`ERROR: This dataset can only be published as a major version.`);
          }
        },
        error: (err) => { console.log('Error') },
        complete: () => {
          this.reviewService.clearDatasets();
          this.router.navigate(['/select']).then(
            () => {
              this.reviewService.updateLocks();
              this.reviewService.updateDatasets();
              publishSubscription.unsubscribe();
            }
          );
        }
      }
    );
  }

  cancelPublish() {
    window.alert('The dataset has NOT been published...');
    this.router.navigate(['/feedback', this.reviewService.selectedDatasetId.value]).then();
  }

  return() {
    this.reviewService.clearDatasets();
    this.reviewService.returnSelected();
    window.alert('The dataset has been returned to author!\n A feedback email has been sent to the author...');
    this.router.navigate(['/select']).then();
  }
  
  cancelReturn() {
    window.alert('The dataset has NOT been returned to the author...');
    this.router.navigate(['/feedback', this.reviewService.selectedDatasetId.value]).then();
  }
}
