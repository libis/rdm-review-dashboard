import { Component, OnInit, AfterViewInit, ViewChild, OnDestroy } from '@angular/core';
import { Dataset } from "../models/dataset";
import { BehaviorSubject, Observable, Subscription } from "rxjs";
import { UserService } from '../services/user.service';
import { FormBuilder } from '@angular/forms';
import { ReviewService } from '../services/review.service';
import { ActivatedRoute, Router } from '@angular/router';
import { ConfirmationService } from 'primeng/api';
import { fromEvent } from 'rxjs';
import { debounceTime, distinctUntilChanged } from 'rxjs/operators';


@Component({
  selector: 'app-dataset-detail',
  templateUrl: './dataset-detail.component.html',
  styleUrls: ['./dataset-detail.component.scss'],
  providers: [ConfirmationService]

})
export class DatasetDetailComponent implements AfterViewInit, OnInit, OnDestroy {
  @ViewChild('notesText') notesTextRef: any;

  dataset: BehaviorSubject<Dataset | null>;
  reviewer$!: Observable<string>;
  noteContent!: string;
  reviewCheckList!: string[];
  searchInput = document.getElementById('notes');
  observable: any;
  noteSubscription!: Subscription;
  routerSubscription!: Subscription;

  notesForm = this.formBuilder.group({
    noteContent: this.noteContent,
  }
  );

  constructor(
    public userService: UserService,
    public reviewService: ReviewService,
    private formBuilder: FormBuilder,
    private router: Router,
    private route: ActivatedRoute,
    private confirmationService: ConfirmationService

  ) {
    this.dataset = this.reviewService.selectedDataset;
    let subscription = this.reviewService.selectedDatasetSavedInternalNote.asObservable().subscribe(
      (noteContent) => {
        this.noteContent = noteContent || '';
        this.updateNoteForm();
        subscription.unsubscribe();
      }
    )
  }

  ngOnInit(): void {
    this.routerSubscription = this.route.params.subscribe(params => {
      let doi = params['datasetId'];
      this.reviewService.selectedDatasetId.next(doi);
    });
  }

  ngAfterViewInit(): void {
    if (this.notesTextRef) {
      this.noteSubscription = fromEvent(this.notesTextRef.nativeElement, 'keyup')
        .pipe(
          debounceTime(1000),
          distinctUntilChanged()
        ).subscribe(
          value => {
            this.saveNotes();
          }

        )
    }
  }


  ngOnDestroy(): void {
  }




  updateNoteForm() {
    this.notesForm.setValue({ noteContent: this.noteContent });
  }


  emptyNotesForm() {
    this.noteContent = ''
    this.updateNoteForm();
  }


  saveNotes() {
    this.reviewService.setInternalNote(this.noteContent);
  }


  loadNotes() {
    this.noteContent = this.reviewService.selectedDatasetSavedInternalNote.value || '';
  }


  clearNotesForm() {
    this.confirmationService.confirm(
      {
        message: `This will replace the current feedback message with one generated from the checklist. Continue?`,
        accept: () => {
          this.noteContent = ''
          this.updateNoteForm();
          this.saveNotes();
        }
      }
    );
  }


  feedback() {
    this.saveNotes();
    this.router.navigate(['feedback', this.dataset.value?.identifier]).then();
  }

}
