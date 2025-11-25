import { Component, OnInit } from '@angular/core';
import { DynamicDialogRef } from 'primeng/dynamicdialog';
import { DynamicDialogConfig } from 'primeng/dynamicdialog';
import { ReviewService } from '../services/review.service';
import { HistoryItem } from '../models/note.model';
@Component({
  selector: 'app-review-history',
  templateUrl: './review-history.component.html',
  styleUrls: ['./review-history.component.scss']
})
export class ReviewHistoryComponent implements OnInit {

  reviewHistory: HistoryItem[] = [];

  constructor(public ref: DynamicDialogRef, public config: DynamicDialogConfig, private reviewService: ReviewService) {
    const subscription = this.reviewService.getHistory().subscribe(
      (history) => {
        this.reviewHistory = history;
        subscription.unsubscribe();
      }
    )
  }

  ngOnInit(): void {
  }

  getSeverity(content: string): "success" | "secondary" | "info" | "warning" | "danger" | "contrast" | undefined {
    let contentLower = content.toLowerCase();
    if (contentLower.includes('publish')) {
      return 'success';
    }
    if (contentLower.includes('return')) {
      return 'danger';
    }
    if (contentLower.includes('deaccession')) {
      return 'danger';
    }
    if (contentLower.includes('assign')) {
      return 'success';
    }
    if (contentLower.includes('delete')) {
      return 'danger';
    }
    if (contentLower.includes('change')) {
      return 'info';
    }
    if (contentLower.includes('reviewer')) {
      return 'secondary';
    }
    if (contentLower.includes('status')) {
      return 'secondary';
    }
    if (contentLower.includes('request')) {
      return 'danger';
    }

    else {
      return 'info'
    }
  }



}
