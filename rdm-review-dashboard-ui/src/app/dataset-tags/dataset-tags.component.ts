import { Component, OnInit, Input } from '@angular/core';
import { Dataset } from '../models/dataset';
import { Style } from '../tag/tag.component';
import { Observable } from 'rxjs';
import { NoteTag } from '../models/note.model';
import { DatasetService } from '../services/dataset.service';

@Component({
  selector: 'app-dataset-tags',
  templateUrl: './dataset-tags.component.html',
  styleUrls: ['./dataset-tags.component.scss']
})
export class DatasetTagsComponent {
  @Input() datasetId!: string;
  @Input() dataset!: Dataset;
  @Input() tags!: NoteTag[]; 
  @Input() observableTags$!: Observable<NoteTag[]>;
  @Input() reviewerTags$!: Observable<NoteTag[]>;
  @Input() tags$!: Observable<NoteTag[]>;
  constructor(private datasetService: DatasetService) { 
}

  getColor(tag: NoteTag) {
    if (tag.content == 'Support Requested') {
      return 'danger';
    }
    if (tag.type == 'status') {
      if (tag.content == 'Submitted for review' || tag.content == 'In review') {
        return 'primary';
      } else {
        return 'secondary';
      } 
    }
    if (tag.type == 'reviewer') {
      if (tag.content == 'Unassigned') {
        return 'primary';
      } else {
        return 'secondary';
      }
    }
    if (tag.type == 'lock') {
      return 'danger';
    }

    return 'primary';
  }



  statusString(): string {
    return Dataset.statusString(this.dataset);
  }

  reviewerString(): string {
    return this.dataset.reviewer.join(', ')
  }

  unitList(): string[] {
    return this.dataset.faculty;
  }


  statusStyle() {
    return (this.statusString()=='Submitted for review' || this.statusString()=='In review') ? Style.Color.Primary : Style.Color.Secondary 
  }

  assignedStyle() {
    return this.reviewerString()=='Unassigned' ? Style.Color.Primary : Style.Color.Secondary 
  }

  capitalizeFirstLetter(s: string): string {
  return s.charAt(0).toUpperCase() + s.slice(1);
  }

}
